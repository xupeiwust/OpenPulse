import numpy as np
from opps.interface.viewer_3d.utils import cross_section_sources
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkIntArray,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import vtkPlane, vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkRenderingCore import vtkActor, vtkGlyph3DMapper

from pulse import app
from pulse.interface.utils import ColorMode
from pulse.interface.viewer_3d.coloring.color_table import ColorTable


class TubeActorGPU(vtkActor):
    """
    This actor show the tubes as a set of element sections that compose it.

    They should appear "sectioned", it is not a bug, it is a feature, because
    the "sections" are correspondent to what is happening in the FEM.

    Usually a model have a lot of elements, and to make this actor render fast,
    this implementations uses vtkGlyph3DMapper, wich is not a traditional approach,
    but is a very fast approach.

    With vtkGlyph3DMapper we just need to create some arrays and very few meshes,
    send them to the GPU, and the hard work is handled there (very fastly btw).
    """

    def __init__(self, project, show_deformed=False, **kwargs) -> None:
        super().__init__()

        self.project = project
        self.model = project.model
        self.preprocessor = project.preprocessor
        self.elements = project.get_structural_elements()
        self.hidden_elements = kwargs.get("hidden_elements", set())
        self.show_deformed = show_deformed

        self.build()

    def build(self):
        visible_elements = {
            i: e for i, e in self.elements.items() if (i not in self.hidden_elements)
        }
        self._key_index = {j: i for i, j in enumerate(visible_elements.keys())}

        data = vtkPolyData()
        mapper = vtkGlyph3DMapper()

        points = vtkPoints()
        sources = vtkIntArray()
        sources.SetName("sources")

        rotations = vtkDoubleArray()
        rotations.SetNumberOfComponents(3)
        rotations.SetName("rotations")

        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetNumberOfTuples(len(visible_elements))
        colors.Fill(255)
        colors.SetName("colors")

        section_index = dict()
        for element in visible_elements.values():
            if self.show_deformed:
                points.InsertNextPoint(*element.first_node.deformed_coordinates)
                rotations.InsertNextTuple(element.deformed_rotation_xyz)
            else:
                points.InsertNextPoint(*element.first_node.coordinates)
                rotations.InsertNextTuple(element.section_rotation_xyz_undeformed)

            key = self._hash_element_section(element)
            if key not in section_index:
                section_index[key] = len(section_index)
                source = self.create_element_data(element)
                source = self._fixed_section(source)
                mapper.SetSourceData(section_index[key], source)
            sources.InsertNextTuple1(section_index[key])

        data.SetPoints(points)
        data.GetPointData().AddArray(sources)
        data.GetPointData().AddArray(rotations)
        data.GetPointData().SetScalars(colors)

        mapper.SetInputData(data)
        mapper.SourceIndexingOn()
        mapper.SetSourceIndexArray("sources")
        mapper.SetOrientationArray("rotations")
        mapper.SetScaleFactor(1)
        mapper.SetOrientationModeToRotation()
        mapper.SetScalarModeToUsePointData()
        mapper.ScalarVisibilityOn()
        mapper.Update()

        self.SetMapper(mapper)

        self.GetProperty().SetInterpolationToPhong()
        self.GetProperty().SetDiffuse(0.8)
        self.GetProperty().SetSpecular(1.5)
        self.GetProperty().SetSpecularPower(80)
        self.GetProperty().SetSpecularColor(1, 1, 1)

    def create_element_data(self, element):
        cross_section = element.cross_section
        if cross_section is None:
            return vtkPolyData()

        # Simplify tube meshes when the model is too big
        if "Pipe section" in cross_section.section_label:
            d_out, t, *_ = cross_section.section_parameters
            return cross_section_sources.pipe_data(element.length, d_out, t, sides=30)

        elif cross_section.section_label == "Rectangular section":
            b, h, t, *_ = cross_section.section_parameters
            return cross_section_sources.rectangular_beam_data(element.length, b, h, t)

        elif cross_section.section_label == "Circular section":
            d_out, t, *_ = cross_section.section_parameters
            return cross_section_sources.circular_beam_data(element.length, d_out, t)

        elif cross_section.section_label == "C-section":
            h, w1, t1, w2, t2, tw, *_ = cross_section.section_parameters
            return cross_section_sources.c_beam_data(
                element.length, h, w1, w2, t1, t2, tw
            )

        elif cross_section.section_label == "I-section":

            h, w1, t1, w2, t2, tw, *_ = cross_section.section_parameters
            return cross_section_sources.i_beam_data(
                element.length, h, w1, w2, t1, t2, tw
            )

        elif cross_section.section_label == "T-section":
            h, w1, t1, tw, *_ = cross_section.section_parameters
            return cross_section_sources.t_beam_data(element.length, h, w1, t1, tw)

        return None

    def clear_colors(self):
        color_mode = app().main_window.visualization_filter.color_mode

        if color_mode == ColorMode.MATERIAL:
            self.color_by_material()

        elif color_mode == ColorMode.FLUID:
            self.color_by_fluid()

        else:
            self.set_color((255, 255, 255))

    def set_color(self, color, elements=None, lines=None):
        # This copy is needed, otherwise the mapper is not updated
        data: vtkPolyData = self.GetMapper().GetInput()
        colors = vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        if (elements is None) and (lines is None):
            for component, value in enumerate(color):
                colors.FillComponent(component, value)
            data.GetPointData().SetScalars(colors)
            self.GetMapper().Update()
            return

        if elements is None:
            elements = set()
        else:
            elements = set(elements)

        # Get the elements inside every entity to paint them
        line_to_elements = self.model.mesh.line_to_elements
        for line in lines:
            line_elements = line_to_elements[line]
            elements |= set(line_elements)

        for element in elements:
            index = self._key_index.get(element)
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def set_color_table(self, color_table: ColorTable):
        # This copy is needed, otherwise the mapper is not updated
        data: vtkPolyData = self.GetMapper().GetInput()
        colors = vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        for i, element in self.elements.items():
            index = self._key_index.get(i)
            if index is None:
                continue
            color = color_table.get_element_color(element)
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def color_by_material(self):
        # This copy is needed, otherwise the mapper is not updated
        data: vtkPolyData = self.GetMapper().GetInput()
        colors = vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        for i, element in self.elements.items():
            index = self._key_index.get(i)
            if index is None:
                continue

            if element.material is None:
                colors.SetTuple(index, (255, 255, 255))
                continue

            # get the element color and make it a bit brighter
            # color = np.array(element.material.getColorRGB()) + 50
            color = np.array(element.material.color) + 50

            color = tuple(np.clip(color, 0, 255))
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def color_by_fluid(self):
        # This copy is needed, otherwise the mapper is not updated
        data: vtkPolyData = self.GetMapper().GetInput()
        colors = vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        for i, element in self.elements.items():
            index = self._key_index.get(i)
            if index is None:
                continue

            if element.fluid is None:
                colors.SetTuple(index, (255, 255, 255))
                continue

            # get the element color and make it a bit brighter
            # color = np.array(element.fluid.getColorRGB()) + 50
            color = np.array(element.fluid.color) + 50

            color = tuple(np.clip(color, 0, 255))
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def apply_cut(self, origin, normal):
        self.plane = vtkPlane()
        self.plane.SetOrigin(origin)
        self.plane.SetNormal(normal)
        self.GetMapper().AddClippingPlane(self.plane)

    def disable_cut(self):
        self.GetMapper().RemoveAllClippingPlanes()

    def _hash_element_section(self, element):
        if element.cross_section is not None:
            section_label = element.cross_section.section_label
            section_parameters = tuple(element.cross_section.section_parameters)
        else:
            section_label = None
            section_parameters = None

        return hash((
            round(element.length, 5),
            section_label,
            section_parameters,
        ))

    def _fixed_section(self, source):
        transform = vtkTransform()
        transform.RotateZ(-90)
        transform.RotateY(180)
        transform.Update()

        transform_filter = vtkTransformFilter()
        transform_filter.SetInputData(source)
        transform_filter.SetTransform(transform)
        transform_filter.Update()

        normals_filter = vtkPolyDataNormals()
        normals_filter.AddInputData(transform_filter.GetOutput())
        normals_filter.Update()

        return normals_filter.GetOutput()
