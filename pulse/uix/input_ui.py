#
from pulse.interface.user_input.project.get_started import GetStartedInput
from pulse.interface.user_input.project.new_project import NewProjectInput
from pulse.interface.user_input.project.load_project import LoadProjectInput
from pulse.interface.user_input.project.reset_project import ResetProjectInput
from pulse.interface.user_input.project.about_open_pulse import AboutOpenPulseInput
#
from pulse.interface.user_input.project.geometryDesignerInput import GeometryDesignerInput
from pulse.interface.user_input.project.editImportedGeometryInput import EditImportedGeometryInput
from pulse.interface.user_input.project.set_project_attributes_input import SetProjectAttributesInput
from pulse.interface.user_input.project.set_geometry_file_input import SetGeometryFileInput
from pulse.interface.user_input.model.setup.general.set_material_input import SetMaterialInput
from pulse.interface.user_input.model.setup.general.fluid_input import FluidInput
from pulse.interface.user_input.model.setup.general.set_cross_section import SetCrossSectionInput
#
from pulse.interface.user_input.model.setup.structural.structuralElementTypeInput import StructuralElementTypeInput
from pulse.interface.user_input.model.setup.structural.dofInput import DOFInput
from pulse.interface.user_input.model.setup.structural.loadsInput import LoadsInput
from pulse.interface.user_input.model.setup.structural.massSpringDamperInput import MassSpringDamperInput
from pulse.interface.user_input.model.setup.structural.elasticNodalLinksInput import ElasticNodalLinksInput
from pulse.interface.user_input.model.setup.structural.set_inertial_load import SetInertialLoad
from pulse.interface.user_input.model.setup.structural.stressStiffeningInput import StressStiffeningInput
from pulse.interface.user_input.model.setup.structural.cappedEndInput import CappedEndInput
from pulse.interface.user_input.model.setup.structural.valvesInput import ValvesInput
from pulse.interface.user_input.model.setup.structural.flangesInput import FlangesInput
from pulse.interface.user_input.model.setup.structural.expansionJointInput import ExpansionJointInput
from pulse.interface.user_input.model.setup.structural.beamXaxisRotationInput import BeamXaxisRotationInput 
from pulse.interface.user_input.model.setup.structural.decouplingRotationDOFsInput import DecouplingRotationDOFsInput
#
from pulse.interface.user_input.model.setup.acoustic.acousticElementTypeInput import AcousticElementTypeInput
from pulse.interface.user_input.model.setup.general.set_fluid_composition_input import SetFluidCompositionInput
from pulse.interface.user_input.model.setup.acoustic.acousticpressureInput import AcousticPressureInput
from pulse.interface.user_input.model.setup.acoustic.volumevelocityInput import VolumeVelocityInput
from pulse.interface.user_input.model.setup.acoustic.specificimpedanceInput import SpecificImpedanceInput
from pulse.interface.user_input.model.setup.acoustic.radiationImpedanceInput import RadiationImpedanceInput
from pulse.interface.user_input.model.setup.acoustic.element_length_correction_input import AcousticElementLengthCorrectionInput
from pulse.interface.user_input.model.setup.acoustic.perforatedPlateInput import PerforatedPlateInput
from pulse.interface.user_input.model.setup.acoustic.compressor_model_input import CompressorModelInput
from pulse.interface.user_input.model.setup.acoustic.check_pulsation_criteria import CheckPulsationCriteriaInput
#
from pulse.interface.user_input.analysis.general.analysis_type import AnalysisTypeInput
from pulse.interface.user_input.analysis.general.analysis_setup import AnalysisSetupInput
from pulse.interface.user_input.analysis.general.run_analysis import RunAnalysisInput
#
from pulse.interface.user_input.plots.structural.plot_structural_mode_shape import PlotStructuralModeShape
from pulse.interface.user_input.plots.structural.plot_displacement_field import PlotDisplacementField
from pulse.interface.user_input.plots.structural.plot_structural_frequency_response import PlotStructuralFrequencyResponse
from pulse.interface.user_input.plots.structural.plot_structural_nodal_results import PlotNodalResultsForStaticAnalysis
from pulse.interface.user_input.plots.structural.plot_reactions import PlotReactions
from pulse.interface.user_input.plots.structural.plot_static_analysis_reactions import PlotStaticAnalysisReactions
from pulse.interface.user_input.plots.structural.plot_stress_field import PlotStressField
from pulse.interface.user_input.plots.structural.plot_stress_field_for_static_analysis import PlotStressFieldForStaticAnalysis
from pulse.interface.user_input.plots.structural.plot_stress_frequency_response_input import PlotStressFrequencyResponseInput
from pulse.interface.user_input.plots.structural.plot_stresses_for_static_analysis import PlotStressesForStaticAnalysis
#
from pulse.interface.user_input.plots.acoustic.plot_acoustic_mode_shape import PlotAcousticModeShape
from pulse.interface.user_input.plots.acoustic.plot_acoustic_pressure_field import PlotAcousticPressureField
from pulse.interface.user_input.plots.acoustic.plot_acoustic_frequency_response_input import PlotAcousticFrequencyResponse
from pulse.interface.user_input.plots.acoustic.plot_acoustic_frequency_response_function import PlotAcousticFrequencyResponseFunctionInput
from pulse.interface.user_input.plots.acoustic.plot_TL_NR_Input import Plot_TL_NR_Input
from pulse.interface.user_input.plots.acoustic.plot_acoustic_delta_pressure_input import PlotAcousticDeltaPressuresInput
from pulse.interface.user_input.plots.acoustic.plotPerforatedPlateConvergenceData import PlotPerforatedPlateConvergenceData
#
from pulse.interface.user_input.plots.structural.plot_cross_section_input import PlotCrossSectionInput
from pulse.interface.user_input.project.render.renderer_user_preferences import RendererUserPreferencesInput
from pulse.interface.user_input.model.info.structuralModel_InfoInput import StructuralModelInfoInput
from pulse.interface.user_input.model.info.acousticModel_InfoInput import AcousticModelInfoInput
from pulse.interface.user_input.model.criteria.checkBeamCriteriaInput import CheckBeamCriteriaInput
#
from pulse.interface.user_input.project.printMessageInput import PrintMessageInput
#
from pulse.uix.clip_plane_widget import ClipPlaneWidget
#
from pulse import app

from time import time

window_title_1 = "Error"
window_title_2 = "Warning"

class InputUi:
    def __init__(self, parent=None):

        self.main_window = parent
        self.project = parent.project
        self.opv = parent.opv_widget
        self.menu_items = parent.model_and_analysis_setup_widget.model_and_analysis_setup_items
        
        self._reset()

    def _reset(self):
        self.analysis_ID = None
        self.global_damping = [0,0,0,0]
        self.project.none_project_action = False

    def beforeInput(self):
        try:
            self.opv.inputObject.close()
            self.opv.setInputObject(None)
        except:
            return

    def processInput(self, workingClass, *args, **kwargs):
        try:
            self.beforeInput()
            read = workingClass(*args, **kwargs)
            self.opv.setInputObject(read)
            return read
        except Exception as log_error:
            title = "Error detected in processInput method"
            message = str(log_error)
            PrintMessageInput([title, message, window_title_1])
            return None

    def new_project(self):
        new_project = self.processInput(NewProjectInput, self.main_window)
        self.main_window._updateStatusBar()
        return self.initial_project_action(new_project.complete)

    def load_project(self, path=None):
        load_project = self.processInput(LoadProjectInput, self.main_window, path=path)
        self.main_window.mesh_toolbar.update_mesh_attributes()
        self.main_window._updateStatusBar()
        return self.initial_project_action(load_project.complete)

    def get_started(self):
        self.menu_items.modify_model_setup_items_access(True)
        get_started = self.processInput(GetStartedInput, self.main_window)
        self.main_window._updateStatusBar()
        # return self.initial_project_action(get_started.complete)          
    
    def initial_project_action(self, finalized):
        app().main_window.action_front_view_callback()
        mesh_setup = self.project.check_mesh_setup()
        if finalized:
            if self.project.empty_geometry:
                self.menu_items.modify_geometry_item_access(False)
                return True
            elif not mesh_setup:
                self.menu_items.modify_general_settings_items_access(False)
                return True   
            else:
                self.project.none_project_action = False
                self.main_window.set_enable_menuBar(True)
                self.menu_items.modify_model_setup_items_access(False) 
                return True
        else:
            self.project.none_project_action = True
            self.menu_items.modify_model_setup_items_access(True)
            return False                 

    def reset_project(self):
        if not self.project.none_project_action:
            self.processInput(ResetProjectInput, self.project, self.opv)

    def set_clipping_plane(self):
        if not self.opv.opvAnalysisRenderer.getInUse():
            return

        clipping_plane = self.processInput(ClipPlaneWidget, self.opv)        
        clipping_plane.value_changed.connect(self.opv.configure_clipping_plane)
        clipping_plane.slider_released.connect(self.opv.apply_clipping_plane)
        clipping_plane.exec()
        self.opv.dismiss_clipping_plane()
            
    def set_project_attributes(self):
        self.processInput(SetProjectAttributesInput, self.project, self.opv)
        self.main_window.changeWindowTitle(self.project.file._project_name)

    def set_geometry_file(self):
        self.processInput(SetGeometryFileInput, self.project, self.opv)

    def call_geometry_designer(self):
        read = self.processInput(GeometryDesignerInput, self.project, self.opv)
        return read.complete

    def call_geometry_editor(self):
        main_window = self.main_window
        main_window.use_geometry_workspace()
        # self.processInput(CreateEditStructuresWidget, self.opv)
        # self.processInput(OPPGeometryDesignerInput, self.project, self.opv)
        # self.initial_project_action(True)

    def edit_an_imported_geometry(self):
        self.opv.Disable()
        read = self.processInput(EditImportedGeometryInput, self.project)
        self.opv.Enable()
        if read.complete:
            self.opv.updatePlots()
            self.opv.changePlotToEntities()
        return read.complete
    
    def get_opv(self):
        return self.opv

    def set_material(self):
        self.processInput(SetMaterialInput, self.project, self.opv)   
         
    def set_cross_section(self, pipe_to_beam=False, beam_to_pipe=False, lines_to_update_cross_section=[]):
        read = self.processInput(   SetCrossSectionInput, 
                                    self.project, 
                                    self.opv, 
                                    pipe_to_beam = pipe_to_beam, 
                                    beam_to_pipe = beam_to_pipe, 
                                    lines_to_update_cross_section = lines_to_update_cross_section   ) 
        return read.complete

    def add_flanges(self):
        self.processInput(FlangesInput, self.project, self.opv)

    def setStructuralElementType(self):
        read = self.processInput(StructuralElementTypeInput, self.project, self.opv)
        if read.complete:
            if read.pipe_to_beam or read.beam_to_pipe:         
                self.set_cross_section( pipe_to_beam=read.pipe_to_beam, beam_to_pipe=read.beam_to_pipe, 
                                        lines_to_update_cross_section=read.list_lines_to_update_cross_section )

    def plot_cross_section(self):
        self.processInput(PlotCrossSectionInput, self.project, self.opv)

    def mesh_setup_visibility(self):
        self.processInput(RendererUserPreferencesInput, self.project, self.opv)
        
    def set_beam_xaxis_rotation(self):
        self.processInput(BeamXaxisRotationInput, self.project, self.opv)
        
    def setDOF(self):
        self.processInput(DOFInput, self.project, self.opv)   
        
    def setRotationDecoupling(self):
        self.processInput(DecouplingRotationDOFsInput, self.project, self.opv)
        
    def setNodalLoads(self):
        self.processInput(LoadsInput, self.project, self.opv)
        
    def addMassSpringDamper(self):
        self.processInput(MassSpringDamperInput, self.project, self.opv)

    def setcappedEnd(self):
        self.processInput(CappedEndInput, self.project, self.opv)

    def set_stress_stress_stiffening(self):
        self.processInput(StressStiffeningInput, self.project, self.opv)

    def add_elastic_nodal_links(self):
        self.processInput(ElasticNodalLinksInput, self.project, self.opv)

    def set_inertial_load(self):
        return self.processInput(SetInertialLoad, self.project)
    
    def add_expansion_joint(self):
        self.processInput(ExpansionJointInput, self.project, self.opv)

    def add_valve(self):
        return self.processInput(ValvesInput, self.project, self.opv)

    def set_acoustic_element_type(self):
        self.processInput(AcousticElementTypeInput, self.project, self.opv)

    def set_fluid(self):
        self.processInput(FluidInput, self.project, self.opv)

    def set_fluid_composition(self):
        self.processInput(SetFluidCompositionInput, self.project, self.opv)

    def setAcousticPressure(self):
        self.processInput(AcousticPressureInput, self.project, self.opv)
    
    def setVolumeVelocity(self):
        self.processInput(VolumeVelocityInput, self.project, self.opv)

    def setSpecificImpedance(self):
        self.processInput(SpecificImpedanceInput, self.project, self.opv)
    
    def set_radiation_impedance(self):
        self.processInput(RadiationImpedanceInput, self.project, self.opv)

    def add_perforated_plate(self):
        self.processInput(PerforatedPlateInput, self.project, self.opv)

    def set_acoustic_element_length_correction(self):
        self.processInput(AcousticElementLengthCorrectionInput, self.project, self.opv)

    def add_compressor_excitation(self):
        self.processInput(CompressorModelInput, self.project, self.opv)

    def check_pulsation_criteria(self):
        self.processInput(CheckPulsationCriteriaInput, self.project, self.opv)

    def analysisTypeInput(self):

        read = self.processInput(AnalysisTypeInput, self.project)

        if not read.complete:
            return

        if read.method_ID == -1:
            return

        self.analysis_ID = self.project.analysis_ID
        self.analysis_type_label = self.project.analysis_type_label
        self.analysis_method_label = self.project.analysis_method_label

        if self.analysis_ID is None:
            self.analysis_ID = None
            return
        
        if self.analysis_ID in [0, 1, 3, 5, 6, 7]:
            self.project.set_structural_solution(None)
            self.project.set_acoustic_solution(None)

        if self.analysis_ID in [2, 4, 7]:
            self.project.update_project_analysis_setup_state(True)
            self.run_analysis()
        else:
            self.analysis_setup()
                    
    def analysis_setup(self):

        if self.project.analysis_ID in [None, 2, 4]:
            return False
        if self.project.file._project_name == "":
            return False
        
        read = self.processInput(AnalysisSetupInput, self.project)
        
        if read.complete:
            if read.flag_run:
                self.run_analysis()
            return True   
        else:
            return False
       
    def run_analysis(self):

        # t0 = time()
        if self.analysis_ID is None or not self.project.setup_analysis_complete:
            
            title = "INCOMPLETE SETUP ANALYSIS" 
            message = "Please, it is necessary to choose an analysis type and \nsetup it before trying to solve the model."
            PrintMessageInput([title, message, window_title_1])
            return

        self.before_run = self.project.get_pre_solution_model_checks(opv=self.opv)
        if self.before_run.check_is_there_a_problem(self.analysis_ID):
            return
        # self.project.time_to_checking_entries = time()-t0

        read = self.processInput(RunAnalysisInput, self.project)
        if read.complete:
            if self.analysis_ID == 2:
                self.before_run.check_modal_analysis_imported_data()
            elif self.analysis_ID in [3, 5, 6]:
                self.before_run.check_all_acoustic_criteria()

            self.after_run = self.project.get_post_solution_model_checks(opv=self.opv)
            self.after_run.check_all_acoustic_criterias()
            self.main_window.use_results_workspace()
        
    def plot_structural_mode_shapes(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = False
        self.project.plot_stress_field = False
        solution = self.project.get_structural_solution()
        if solution is None:
            return None
        if self.analysis_ID in [2, 4]:
            return self.processInput(PlotStructuralModeShape)      

    def plot_displacement_field(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = False
        self.project.plot_stress_field = False
        solution = self.project.get_structural_solution()
        if self.analysis_ID in [0, 1, 5, 6, 7]:
            if solution is None:
                return None
            return self.processInput(PlotDisplacementField)

    def plot_acoustic_mode_shapes(self):
        self.project.plot_pressure_field = True
        self.project.plot_stress_field = False
        solution = self.project.get_acoustic_solution()
        if solution is None:
            return None
        if self.analysis_ID in [2, 4]:
            return self.processInput(PlotAcousticModeShape)           

    def plot_acoustic_pressure_field(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = True
        self.project.plot_stress_field = False
        solution = self.project.get_acoustic_solution()
        if self.analysis_ID in [3,5,6]:
            if solution is None:
                return None
            return self.processInput(PlotAcousticPressureField)           

    def plot_structural_frequency_response(self):
        if self.analysis_ID in [0, 1, 5, 6, 7]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return None
            if self.analysis_ID == 7:
                return self.processInput(PlotNodalResultsForStaticAnalysis)
            else:
                return self.processInput(PlotStructuralFrequencyResponse)

    def plot_acoustic_frequency_response(self):
        if self.analysis_ID in [3, 5, 6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return None
            return self.processInput(PlotAcousticFrequencyResponse)

    def plot_acoustic_frequency_response_function(self):
        if self.analysis_ID in [3,5,6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return None
            return self.processInput(  PlotAcousticFrequencyResponseFunctionInput, self.project, self.opv)

    def plotAcousticDeltaPressures(self):
        if self.analysis_ID in [3,5,6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return None
            return self.processInput(  PlotAcousticDeltaPressuresInput, 
                                self.project, 
                                self.opv  )

    def plot_TL_NR(self):
        if self.analysis_ID in [3,5,6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return
            self.processInput(  Plot_TL_NR_Input, 
                                self.project, 
                                self.opv  )

    def plotPerforatedPlateConvergenceDataLog(self):
        if self.project.perforated_plate_dataLog:
            self.processInput( PlotPerforatedPlateConvergenceData, self.project.perforated_plate_dataLog )

    def plot_stress_field(self):
        self.project.plot_pressure_field = False
        self.project.plot_stress_field = True
        if self.analysis_ID in [0, 1, 5, 6, 7]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return
            if self.analysis_ID == 7:
                self.processInput(PlotStressFieldForStaticAnalysis, self.project, self.opv)
            else:
                self.processInput(PlotStressField, self.project, self.opv)

    def plotStressFrequencyResponse(self):
        solution = self.project.get_structural_solution()
        if solution is None:
            return
        if self.analysis_ID == 7:
            self.processInput(PlotStressesForStaticAnalysis, 
                              self.project, 
                              self.opv)
        elif self.analysis_ID in [0, 1, 5, 6]:
            self.processInput(PlotStressFrequencyResponseInput, 
                              self.project, 
                              self.opv)

    def plotReactionsFrequencyResponse(self):
        if self.analysis_ID in [0, 1, 5, 6]:
            self.processInput(PlotReactions, self.project, self.opv)
        elif self.analysis_ID == 7:
            self.processInput(PlotStaticAnalysisReactions, self.project, self.opv)

    def structural_model_info(self):
        self.processInput(StructuralModelInfoInput, self.project, self.opv)

    def acoustic_model_info(self):
        self.processInput(AcousticModelInfoInput, self.project, self.opv)

    def check_beam_criteria(self):
        self.processInput(CheckBeamCriteriaInput, self.project, self.opv)

    def about_OpenPulse(self):
        self.processInput(AboutOpenPulseInput, self.project, self.opv)

    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = 'Please, you should create a new project or load an already existing one before start to set up the model.'
        message += "\n\nIt is recommended to use the 'New Project' or the 'Import Project' buttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([title, message, window_title])