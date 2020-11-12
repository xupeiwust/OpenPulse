import vtk
import numpy as np 
from time import time

from pulse.interface.vtkActorBase import vtkActorBase

class TubeActor(vtkActorBase):
    def __init__(self, elements, project, deformation=None, colorTable=None):
        super().__init__()

        self.elements = elements
        self.project = project

        self.deformation = deformation
        self.colorTable = colorTable

        self._appendData = vtk.vtkAppendPolyData()
        self._mapper = vtk.vtkPolyDataMapper()

        self._cachePolygon = dict()
        self._cacheMatrix = dict()
    
    def source(self):
        sections = [self.createTubeSection(element) for element in self.elements]
        matrices = [self.createMatrix(element) for element in self.elements] 
        colors = [self.normalizeColor(element) for element in self.elements]
        self._appendData = self.generateTube(sections, matrices, colors)
        
    def filter(self):
        pass
    
    def map(self):
        self._appendData.Update()
        self._mapper.SetInputData(self._appendData.GetOutput())
    
    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().BackfaceCullingOff()
        self._actor.GetProperty().LightingOff()
        self._actor.GetProperty().ShadingOff()

    def normalizeColor(self, element):
        if self.colorTable is None:
            return (255,255,255)
        else:
            return self.colorTable.get_color_by_id(element.index)

    def createTubeSection(self, element):
        if element.cross_section in self._cachePolygon:
            return self._cachePolygon[element.cross_section]   
    
        NUMBER_OF_SIDES = 20
        MINIMUM_RADIUS = 0.01

        if not element.cross_section:
            polygon = vtk.vtkRegularPolygonSource()
            polygon.SetNumberOfSides(NUMBER_OF_SIDES)
            polygon.SetRadius(MINIMUM_RADIUS)
        else:
            label, parameters, *args = element.cross_section.additional_section_info
            if label == "Pipe section":
                polygon = vtk.vtkRegularPolygonSource()
                polygon.SetNumberOfSides(NUMBER_OF_SIDES)
                polygon.SetRadius(element.cross_section.external_diameter / 2)
            else:
                polygon = self.createSectionPolygon(element)
        
        self._cachePolygon[element.cross_section] = polygon
        return polygon

    def createSectionPolygon(self, element):
        points = vtk.vtkPoints()
        edges = vtk.vtkCellArray()
        polygon = vtk.vtkPolygon()
        polyData = vtk.vtkPolyData()
        triangleFilter = vtk.vtkTriangleFilter() # this prevents bugs on extruder

        Xs, Ys = self.project.get_mesh().get_cross_section_points(element.index)
        polygon.GetPointIds().SetNumberOfIds(len(Xs))
        
        for i, (x, y) in enumerate(zip(Xs, Ys)):
            points.InsertNextPoint(x, y, 0)
            polygon.GetPointIds().SetId(i,i)
        edges.InsertNextCell(polygon)

        polyData.SetPoints(points)
        polyData.SetPolys(edges)
        triangleFilter.AddInputData(polyData)
        return triangleFilter
    
    def createMatrix(self, element):
        vec = tuple(element.last_node.coordinates - element.first_node.coordinates)

        if vec in self._cacheMatrix:
            # this cache may not look so usefull here
            # but it acelerates self._appendData.Update() 
            scale, rotation = self._cacheMatrix[vec]
        else:
            scale = self.createScaleMatrix(element)
            rotation = self.createRotationMatrix(element)
            self._cacheMatrix[vec] = scale, rotation

        translation = self.createTranslationMatrix(element)
        final = (rotation + translation) * scale
        
        matrix = vtk.vtkMatrix4x4()
        matrix.DeepCopy(final.flatten()) # numpy to vtk
        return matrix

    def createRotationMatrix(self, element):
        u,v,w = element.inverse_sub_rotation_matrix.T # directional vectors
        matrix = np.identity(4)
        matrix[0:3, 0] = v
        matrix[0:3, 1] = w
        matrix[0:3, 2] = u 
        return matrix

    def createTranslationMatrix(self, element):
        start = element.first_node.coordinates
        matrix = np.zeros((4,4))
        matrix[0:3, 3] = start 
        return matrix
    
    def createScaleMatrix(self, element):
        size = element.length
        matrix = np.ones((4,4))
        matrix[:, 2] = size
        return matrix
    
    def generateTube(self, sections, matrices, colors):
        # this may be the most costly function and should be implemented in c++ 
        data = vtk.vtkAppendPolyData()
        for section, matrix, color in zip(sections, matrices, colors):
            transformation = vtk.vtkTransform()
            extruderFilter = vtk.vtkLinearExtrusionFilter()
            transformPolyDataFilter = vtk.vtkTransformPolyDataFilter()

            transformation.Concatenate(matrix)
            extruderFilter.SetInputConnection(section.GetOutputPort())
            transformPolyDataFilter.SetInputConnection(extruderFilter.GetOutputPort())
            transformPolyDataFilter.SetTransform(transformation)
            transformPolyDataFilter.Update()

            tube = transformPolyDataFilter.GetOutput()
            self.paint(tube, color)
            data.AddInputData(tube)
        return data

    def paint(self, data, color):
        faces = data.GetNumberOfCells()
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetNumberOfTuples(faces)

        for i in range(faces):
            colors.SetTuple(i, color)
        data.GetCellData().SetScalars(colors)