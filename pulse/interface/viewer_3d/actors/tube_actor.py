import vtk


class TubeActor(vtk.vtkActor):
    def __init__(self, project, **kwargs) -> None:
        super().__init__()

        self.project = project
        self.preprocessor = project.preprocessor
        self.elements = project.get_structural_elements()
        self.hidden_elements = kwargs.get('hidden_elements', set())

        self.build()

    def build(self):
        visible_elements = {i:e for i, e in self.elements.items() if (i not in self.hidden_elements)}
        # self._key_index  = {j:i for i,j in enumerate(visible_elements)}
        self._key_indexes = dict()

        mapper = vtk.vtkPolyDataMapper()
        append_polydata = vtk.vtkAppendPolyData()

        total_points_appended = 0 
        for i, element in visible_elements.items():            
            x,y,z = element.first_node.coordinates
            section_rotation_xyz = element.section_rotation_xyz_undeformed

            source = self.create_element_data(element)
            self._key_indexes[i] = range(total_points_appended, total_points_appended + source.GetNumberOfPoints())
            total_points_appended += source.GetNumberOfPoints()

            # for _ in range(source.GetNumberOfPoints()):
            #     self._colors.InsertNextTuple((255,255,255))

            transform = vtk.vtkTransform()
            transform.Translate((x,y,z))
            transform.RotateX(section_rotation_xyz[0])
            transform.RotateZ(section_rotation_xyz[2])
            transform.RotateY(section_rotation_xyz[1])
            transform.RotateZ(90)

            transform.Update()

            transform_filter = vtk.vtkTransformFilter()
            transform_filter.SetInputData(source)
            transform_filter.SetTransform(transform)
            transform_filter.Update()

            append_polydata.AddInputData(transform_filter.GetOutput())
        
        append_polydata.Update()
        mapper.SetInputData(append_polydata.GetOutput())
        self.SetMapper(mapper)

    def create_element_data(self, element):
        return self.c_beam_data(element.length, 0.08, 0.04, 0.06, 0.005, 0.005, 0.005)
        # sphere = vtk.vtkSphereSource()
        # sphere.SetRadius(0.1)
        # sphere.Update()
        # return sphere.GetOutput()

    def pipe_data(self, length, outside_diameter, thickness):
        if thickness == 0:
            return self.closed_pipe_data(length, outside_diameter)
        cilinder = vtk.vtkCylinderSource()
        cilinder.SetResolution(20)
        cilinder.SetRadius(outside_diameter / 2)
        cilinder.SetHeight(length)
        cilinder.CappingOff()
        cilinder.Update()
        return cilinder.GetOutput()

    def closed_pipe_data(self, length, outside_diameter):
        cilinder = vtk.vtkCylinderSource()
        cilinder.SetResolution(20)
        cilinder.SetRadius(outside_diameter / 2)
        cilinder.SetHeight(length)
        cilinder.CappingOn()
        cilinder.Update()
        return cilinder.GetOutput()

    def circular_beam_data(self, length, outside_diameter, thickness):
        return self.pipe_data(length, outside_diameter, thickness)

    def square_beam_data(self, length, b, h, t):
        if t == 0:
            return self.closed_square_beam_data(length, b, h)

        square_top = vtk.vtkCubeSource()
        square_left = vtk.vtkCubeSource()
        square_right = vtk.vtkCubeSource()
        square_bottom = vtk.vtkCubeSource()

        square_top.SetYLength(length)
        square_top.SetZLength(t)
        square_top.SetXLength(b)
        square_top.SetCenter(0, 0, -h/2 + t/2)

        square_left.SetYLength(length)
        square_left.SetZLength(h)
        square_left.SetXLength(t)
        square_left.SetCenter(-b/2 + t/2, 0, 0)

        square_right.SetYLength(length)
        square_right.SetZLength(h)
        square_right.SetXLength(t)
        square_right.SetCenter(b/2 - t/2, 0, 0)

        square_bottom.SetYLength(length)
        square_bottom.SetZLength(t)
        square_bottom.SetXLength(b)
        square_bottom.SetCenter(0, 0, h/2 - t/2)

        square_top.Update()
        square_left.Update()
        square_right.Update()
        square_bottom.Update()

        append_polydata = vtk.vtkAppendPolyData()
        append_polydata.AddInputData(square_top.GetOutput())
        append_polydata.AddInputData(square_left.GetOutput())
        append_polydata.AddInputData(square_right.GetOutput())
        append_polydata.AddInputData(square_bottom.GetOutput())
        append_polydata.Update()

        return append_polydata.GetOutput()

    def closed_square_beam_data(self, length, b, h):
        square = vtk.vtkCubeSource()
        square.SetYLength(length)
        square.SetXLength(b)
        square.SetZLength(h)
        square.Update()
        return square.GetOutput()

    def c_beam_data(self, length, h, w1, w2, t1, t2, tw):
        square_top = vtk.vtkCubeSource()
        square_left = vtk.vtkCubeSource()
        square_bottom = vtk.vtkCubeSource()

        square_top.SetYLength(length)
        square_top.SetZLength(t1)
        square_top.SetXLength(w1)
        square_top.SetCenter(w1/2 - max(w1, w2)/2, 0, -h/2 + t1/2)

        square_left.SetYLength(length)
        square_left.SetZLength(h)
        square_left.SetXLength(tw)
        square_left.SetCenter(-max(w1, w2)/2 + tw/2, 0, 0)

        square_bottom.SetYLength(length)
        square_bottom.SetZLength(t2)
        square_bottom.SetXLength(w2)
        square_bottom.SetCenter(w2/2 - max(w1, w2)/2, 0, h/2 - t2/2)

        square_top.Update()
        square_left.Update()
        square_bottom.Update()

        append_polydata = vtk.vtkAppendPolyData()
        append_polydata.AddInputData(square_top.GetOutput())
        append_polydata.AddInputData(square_left.GetOutput())
        append_polydata.AddInputData(square_bottom.GetOutput())
        append_polydata.Update()

        return append_polydata.GetOutput()

    def i_beam_data(self, length, h, w1, w2, t1, t2, tw):
        square_top = vtk.vtkCubeSource()
        square_center = vtk.vtkCubeSource()
        square_bottom = vtk.vtkCubeSource()

        square_top.SetYLength(length)
        square_top.SetZLength(t1)
        square_top.SetXLength(w1)
        square_top.SetCenter(0, 0, -h/2 + t1/2)

        square_center.SetYLength(length)
        square_center.SetZLength(h)
        square_center.SetXLength(tw)

        square_bottom.SetYLength(length)
        square_bottom.SetZLength(t2)
        square_bottom.SetXLength(w2)
        square_bottom.SetCenter(0, 0, h/2 - t2/2)

        square_top.Update()
        square_center.Update()
        square_bottom.Update()

        append_polydata = vtk.vtkAppendPolyData()
        append_polydata.AddInputData(square_top.GetOutput())
        append_polydata.AddInputData(square_center.GetOutput())
        append_polydata.AddInputData(square_bottom.GetOutput())
        append_polydata.Update()

        return append_polydata.GetOutput()

    def t_beam_data(self, length, h, w1, t1, tw):
        square_top = vtk.vtkCubeSource()
        square_center = vtk.vtkCubeSource()

        square_top.SetYLength(length)
        square_top.SetZLength(t1)
        square_top.SetXLength(w1)
        square_top.SetCenter(0, 0, -h/2 + t1/2)

        square_center.SetYLength(length)
        square_center.SetZLength(h)
        square_center.SetXLength(tw)

        square_top.Update()
        square_center.Update()

        append_polydata = vtk.vtkAppendPolyData()
        append_polydata.AddInputData(square_top.GetOutput())
        append_polydata.AddInputData(square_center.GetOutput())
        append_polydata.Update()

        return append_polydata.GetOutput()
