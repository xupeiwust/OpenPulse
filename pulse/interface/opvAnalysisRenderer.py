from data.user_input.project.printMessageInput import PrintMessageInput
import vtk
import numpy as np

from pulse.postprocessing.plot_structural_data import get_structural_response
from pulse.postprocessing.plot_acoustic_data import get_acoustic_response

from pulse.uix.vtk.colorTable import ColorTable
from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkMeshClicker import vtkMeshClicker
from pulse.interface.tubeActor import TubeActor
from pulse.interface.symbolsActor import SymbolsActor
from pulse.interface.tubeDeformedActor import TubeDeformedActor
from threading import Thread


class opvAnalysisRenderer(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkMeshClicker(self))

        self.project = project
        self.opv = opv
        self.setUsePicker(False)

        self._magnificationFactor = 1
        self._currentFrequencyIndex = 0
        self._cacheFrequencyIndex = None
        self.lastFrequency = None
        self.scf = None
        self._currentPlot = None
        self.colorbar = None 
        self.scaleBar = None

        self.playingAnimation = False
        self.animationTimer = 0
        self.dt = 0.05

        # just ignore it 
        self.nodesBounds = dict()
        self.elementsBounds = dict()
        self.lineToElements = dict()

        self.opvDeformedTubes = None
        self.opvPressureTubes = None
        self.opvSymbols = None

        self.slider = None
        self._createSlider()
        self._createPlayer()
        self._animationFrames = dict()

    def plot(self):
        self.reset()

        self.opvDeformedTubes = TubeDeformedActor(self.project.get_structural_elements(), self.project)
        self.opvPressureTubes = TubeActor(self.project.get_structural_elements(), self.project, pressure_plot=True)
        self.opvSymbols = SymbolsActor(self.project.get_nodes(), self.project, deformed=True)

        self.opvPressureTubes.transparent = False

        self._createSlider()
        plt = lambda x: self._renderer.AddActor(x.getActor())
        plt(self.opvDeformedTubes)
        plt(self.opvPressureTubes)
        plt(self.opvSymbols)
    
    def reset(self):
        self._renderer.RemoveAllViewProps()
        self._style.clear()

    def setInUse(self, *args, **kwargs):
        super().setInUse(*args, **kwargs)
        self.pauseAnimation()
    
    def update(self):
        self.opv.updateDialogs()
        renWin = self._renderer.GetRenderWindow()
        if renWin: renWin.Render()

    def updateHud(self):
        self._createSlider()
        self._createColorBar()
        self._createScaleBar()

    def _cacheFrames(self, single_frame=False, value=1):
        if single_frame:
            vals = [value]
        else:
            vals = [round(i/10, 1) for i in range(-10, 11)]  
        for val in vals:
            self._currentPlot(self._currentFrequencyIndex, val)
            cached = vtk.vtkPolyData()
            cached.DeepCopy(self.opvDeformedTubes._data)
            self._animationFrames[val] = cached

    def _plotCached(self, gain):
        cached = self._animationFrames[round(gain, 1)]
        self.opvDeformedTubes._data.DeepCopy(cached)
        self.updateInfoText()
        self.update_min_max_stresses_text()
        self.opv.update()
        self._renderer.ResetCameraClippingRange()
        self.update()

    def showDisplacement(self, frequency_index):
        self._currentPlot = self.computeDisplacement
        self._currentFrequencyIndex = frequency_index   
        self._animationFrames.clear()
        self._cacheFrames(single_frame=True)
        self._plotCached(1)

    def showStressField(self, frequency_index):
        self._currentPlot = self.computeStressField
        self._currentFrequencyIndex = frequency_index    
        self._animationFrames.clear()
        self._cacheFrames(single_frame=True)
        self._plotCached(1)

    def showPressureField(self, frequency_index, real_part=True):
        self.computePressureField(frequency_index, real_part=True)
        self.updateInfoText()
        self.update_min_max_stresses_text()
        self._renderer.ResetCameraClippingRange()
        self.opv.update()
        self.update()

    def computeDisplacement(self, frequency, gain=1):
        preprocessor = self.project.preprocessor
        solution = self.project.get_structural_solution()    
        _, _, u_def, self._magnificationFactor, scf = get_structural_response(  preprocessor, 
                                                                                solution, 
                                                                                frequency, 
                                                                                gain=gain,
                                                                                new_scf=self.scf   )
        self.opvDeformedTubes.build()

        colorTable = ColorTable(self.project, u_def)
        self.opvDeformedTubes.setColorTable(colorTable)
        self.colorbar.SetLookupTable(colorTable)

        self.slider.SetEnabled(True)
        self.opvDeformedTubes.getActor().SetVisibility(True)
        self.opvPressureTubes.getActor().SetVisibility(False)

    def computeStressField(self, frequency, gain=1):
        preprocessor = self.project.preprocessor
        solution = self.project.get_structural_solution()
        _, _, _, self._magnificationFactor, scf = get_structural_response(  preprocessor, 
                                                                            solution, 
                                                                            frequency, 
                                                                            gain=gain,
                                                                            new_scf=self.scf   )
        self.opvDeformedTubes.build()

        colorTable = ColorTable(self.project, self.project.stresses_values_for_color_table, stress_field_plot=True)
        self.opvDeformedTubes.setColorTable(colorTable)
        self.colorbar.SetLookupTable(colorTable)
        
        self.slider.SetEnabled(True)
        self.opvDeformedTubes.getActor().SetVisibility(True)
        self.opvPressureTubes.getActor().SetVisibility(False)

    def computePressureField(self, frequency, real_part=True):

        preprocessor = self.project.preprocessor
        solution = self.project.get_acoustic_solution()
        self._currentFrequencyIndex = frequency
        self._colorScalling = 'real part' if real_part else 'absolute'

        *args, pressure_field_data = get_acoustic_response(preprocessor, solution, frequency, real_part)
        self.opvPressureTubes.build()

        colorTable = ColorTable(self.project, pressure_field_data, pressure_field_plot=True)
        self.opvPressureTubes.setColorTable(colorTable)
        self.colorbar.SetLookupTable(colorTable)
        
        self.slider.SetEnabled(False)
        self.opvDeformedTubes.getActor().SetVisibility(False)
        self.opvPressureTubes.getActor().SetVisibility(True)

    def _createSlider(self):
        self.slider = vtk.vtkSliderWidget()
        
        sld = vtk.vtkSliderRepresentation2D()
        sld.SetMinimumValue(-1)
        sld.SetMaximumValue(1)
        sld.SetValue(1)

        sld.GetSelectedProperty().SetColor(1, 0, 0)
        sld.GetTubeProperty().SetColor(0.5, 0.5, 0.5)
        sld.GetCapProperty().SetColor(0.8, 0.8, 0.8)
        
        sld.SetSliderLength(0.01)
        sld.SetSliderWidth(0.02)
        sld.SetTubeWidth(0.02)

        sld.SetEndCapWidth(0.02)
        sld.SetEndCapLength(0.005)

        sld.SetTitleHeight(0.015)
        sld.SetLabelHeight(0.015)

        width, height = self.getSize()
        sld.GetPoint1Coordinate().SetCoordinateSystemToDisplay()
        sld.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
        sld.GetPoint1Coordinate().SetValue(20, height-150)
        sld.GetPoint2Coordinate().SetValue(220, height-150)

        self.slider.SetInteractor(self.opv)
        self.slider.SetRepresentation(sld)
        self.slider.AddObserver(vtk.vtkCommand.EndInteractionEvent, self._sliderCallback)

    def _createPlayer(self):
        self.opv.Initialize()
        self.opv.CreateRepeatingTimer(1000 * 100)
        self.opv.AddObserver('TimerEvent', self._animationCallback)

    def playAnimation(self):
        self.animationTimer = self.slider.GetRepresentation().GetValue()
        self.playingAnimation = True

    def pauseAnimation(self):
        self.playingAnimation = False

    def tooglePlayPauseAnimation(self):
        if self.project.analysis_ID not in [3,4] and not self.project.plot_pressure_field:
            self.playingAnimation = not self.playingAnimation
            if self.playingAnimation:
                if self._cacheFrequencyIndex != self._currentFrequencyIndex:
                    self._animationFrames.clear()
                    #TODO: print the log message while the calculation is in progress then close it automatically after all
                    self.printLogMessage()
                    # self._cacheFrames()
                    self._cacheFrequencyIndex = self._currentFrequencyIndex
    
    def printLogMessage(self):
        title = "Processing in progress"
        message = "The animation frames calculation in progress." 
        PrintMessageInput([title, message, "OpenPulse"], opvAnalysisRenderer=self)

    def _animationCallback(self, caller, event):
        if self._currentPlot is None:
            return 

        if not self.playingAnimation:
            return

        self.animationTimer += self.dt

        if self.animationTimer <= -1:
            self.dt = -self.dt 
            self.animationTimer = -1
        
        elif self.animationTimer >= 1:
            self.dt = -self.dt
            self.animationTimer = 1

        self.slider.GetRepresentation().SetValue(round(self.animationTimer, 1))
        self._plotCached(self.animationTimer)

    def _sliderCallback(self, slider, b):
        if self._currentPlot is None:
            return 
        
        self.playingAnimation = False
        sliderValue = slider.GetRepresentation().GetValue()
        slider.GetRepresentation().SetValue(round(sliderValue, 1))
        self._cacheFrames(single_frame=True, value=round(sliderValue, 1))
        self._plotCached(sliderValue)

    def _createColorBar(self):
        textProperty = vtk.vtkTextProperty()
        textProperty.SetFontSize(14)
        textProperty.SetItalic(1)
        unit = self.project.get_unit()
        text = "Unit: [{}]".format(unit)

        self._renderer.RemoveActor(self.colorbar)
        self.colorbar = vtk.vtkScalarBarActor()
        self.colorbar.SetLabelTextProperty(textProperty)
        self.colorbar.SetMaximumNumberOfColors(400)
        self.colorbar.SetWidth(0.04)
        self.colorbar.SetTextPositionToPrecedeScalarBar()
        self.colorbar.SetPosition(0.94, 0.1)
        self.colorbar.SetLabelFormat("%1.0e ")
        self.colorbar.UnconstrainedFontSizeOn()   
        self.colorbar.VisibilityOn()
        self.colorbar.SetTitle(text)
        self.colorbar.SetVerticalTitleSeparation(20)
        self.colorbar.GetTitleTextProperty().SetFontSize(20)
        self.colorbar.GetTitleTextProperty().SetJustificationToLeft()
        self._renderer.AddActor(self.colorbar)

    def _createScaleBar(self):
        width, height = self.getSize()
        self._renderer.RemoveActor(self.scaleBar)
        self.scaleBar = vtk.vtkLegendScaleActor()
        self.scaleBar.AllAxesOff()
        self._renderer.AddActor(self.scaleBar)

    # info text
    def updateInfoText(self, *args, **kwargs):
        mode = self._currentFrequencyIndex + 1
        magnif = abs(self.slider.GetRepresentation().GetValue())
        frequencies = self.project.get_frequencies()
        text = self.project.analysis_type_label + "\n"
        if self.project.analysis_ID not in [2,4]:
            text += self.project.analysis_method_label + "\n"
            text += "Frequency: {:.2f} [Hz]\n".format(frequencies[self._currentFrequencyIndex])
        elif self.project.analysis_ID == 2:
            frequencies = self.project.get_structural_natural_frequencies()
            text += "Mode: {}\n".format(mode)
            text += "Natural Frequency: {:.2f} [Hz]\n".format(frequencies[self._currentFrequencyIndex])
        elif self.project.analysis_ID == 4:
            frequencies = self.project.get_acoustic_natural_frequencies()
            text += "Mode: {}\n".format(mode)
            text += "Natural Frequency: {:.2f} [Hz]\n".format(frequencies[self._currentFrequencyIndex])
            text += "Color scalling: {}".format(self._colorScalling)
        if not self.project.plot_pressure_field:
            text += "\nMagnification factor: {:.4e}\n".format(self._magnificationFactor)
        # vertical_position_adjust = None
        self.createInfoText(text)

    def update_min_max_stresses_text(self):
                
        min_stress = self.project.min_stress
        max_stress = self.project.max_stress
        stress_label = self.project.stress_label

        text = ""
        if self.project.min_stress != "" and self.project.max_stress != "":
            text += "Maximum {} stress: {:.3e} [Pa]\n".format(stress_label, max_stress)
            text += "Minimum {} stress: {:.3e} [Pa]\n".format(stress_label, min_stress)

        self.textActorStress.SetInput(text)
        textProperty = vtk.vtkTextProperty()
        textProperty.SetFontSize(17)
        textProperty.SetBold(1)
        textProperty.SetItalic(1)
        self.textActorStress.SetTextProperty(textProperty)
        _, height = self._renderer.GetSize()
        self.textActorStress.SetDisplayPosition(600, height-75)
        self._renderer.AddActor2D(self.textActorStress)

    # functions to be removed but currently break the execution
    def getElementsInfoText(self, *args, **kwargs):
        pass
    
    def getEntityInfoText(self, *args, **kwargs):
        pass 

    def getPlotRadius(self, *args, **kwargs):
        return 
    
    def changeColorEntities(self, *args, **kwargs):
        return 

    def setPlotRadius(self, plt):
        pass