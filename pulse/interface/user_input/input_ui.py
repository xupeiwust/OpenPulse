#
from pulse.interface.user_input.model.geometry.geometry_editor_help import GeometryEditorHelp
#
from pulse.interface.user_input.model.setup.material.set_material_input import SetMaterialInput
from pulse.interface.user_input.model.setup.fluid.set_fluid_input import SetFluidInput
from pulse.interface.user_input.model.setup.cross_section.set_cross_section import SetCrossSectionInput
#
from pulse.interface.user_input.model.setup.structural.structural_element_type_input import StructuralElementTypeInput
from pulse.interface.user_input.model.setup.structural.prescribed_dofs_input import PrescribedDofsInput
from pulse.interface.user_input.model.setup.structural.nodal_loads_input import NodalLoadsInput
from pulse.interface.user_input.model.setup.structural.mass_spring_damper_input import MassSpringDamperInput
from pulse.interface.user_input.model.setup.structural.elastic_nodal_links_input import ElasticNodalLinksInput
from pulse.interface.user_input.model.setup.structural.set_inertial_load import SetInertialLoad
from pulse.interface.user_input.model.setup.structural.stress_stiffening_input import StressStiffeningInput
from pulse.interface.user_input.model.setup.structural.capped_end_input import CappedEndInput
from pulse.interface.user_input.model.setup.structural.set_valves_input import ValvesInput
from pulse.interface.user_input.model.setup.structural.connecting_flanges_input import ConnectingFlangesInput
from pulse.interface.user_input.model.setup.structural.expansion_joint_input import ExpansionJointInput
from pulse.interface.user_input.model.setup.structural.xaxis_beam_rotation_input import BeamXaxisRotationInput 
from pulse.interface.user_input.model.setup.structural.decoupling_rotation_dofs_input import DecouplingRotationDOFsInput
#
from pulse.interface.user_input.model.setup.acoustic.acoustic_element_type_input import AcousticElementTypeInput
from pulse.interface.user_input.model.setup.fluid.set_fluid_composition_input import SetFluidCompositionInput
from pulse.interface.user_input.model.setup.acoustic.acoustic_pressure_input import AcousticPressureInput
from pulse.interface.user_input.model.setup.acoustic.volume_velocity_input import VolumeVelocityInput
from pulse.interface.user_input.model.setup.acoustic.specific_impedance_input import SpecificImpedanceInput
from pulse.interface.user_input.model.setup.acoustic.radiation_impedance_input import RadiationImpedanceInput
from pulse.interface.user_input.model.setup.acoustic.element_length_correction_input import AcousticElementLengthCorrectionInput
from pulse.interface.user_input.model.setup.acoustic.perforated_plate_input import PerforatedPlateInput
from pulse.interface.user_input.model.setup.acoustic.compressor_model_input import CompressorModelInput
from pulse.interface.user_input.model.editor.pulsation_suppression_device_input import PulsationSuppressionDeviceInput
from pulse.interface.user_input.model.criteria.check_pulsation_criteria import CheckAPI618PulsationCriteriaInput
from pulse.interface.user_input.model.criteria.shaking_forces_criteria import ShakingForcesCriteriaInput
#
from pulse.interface.user_input.analysis.general.analysis_type import AnalysisTypeInput
from pulse.interface.user_input.analysis.general.analysis_setup import AnalysisSetupInput
from pulse.interface.user_input.analysis.general.run_analysis import RunAnalysisInput
#
from pulse.interface.user_input.plots.structural.plot_structural_mode_shape import PlotStructuralModeShape
from pulse.interface.user_input.plots.structural.plot_nodal_results_field_for_harmonic_analysis import PlotNodalResultsFieldForHarmonicAnalysis
from pulse.interface.user_input.plots.structural.plot_nodal_results_for_harmonic_analysis import PlotNodalResultsForHarmonicAnalysis
from pulse.interface.user_input.plots.structural.plot_nodal_results_for_static_analysis import PlotNodalResultsForStaticAnalysis
from pulse.interface.user_input.plots.structural.plot_reactions_for_harmonic_analysis import PlotReactionsForHarmonicAnalysis
from pulse.interface.user_input.plots.structural.plot_reactions_for_static_analysis import PlotReactionsForStaticAnalysis
from pulse.interface.user_input.plots.structural.plot_stresses_field_for_harmonic_analysis import PlotStressesFieldForHarmonicAnalysis
from pulse.interface.user_input.plots.structural.plot_stress_field_for_static_analysis import PlotStressesFieldForStaticAnalysis
from pulse.interface.user_input.plots.structural.plot_stresses_for_harmonic_analysis import PlotStressesForHarmonicAnalysis
from pulse.interface.user_input.plots.structural.plot_stresses_for_static_analysis import PlotStressesForStaticAnalysis
#
from pulse.interface.user_input.plots.acoustic.plot_acoustic_mode_shape import PlotAcousticModeShape
from pulse.interface.user_input.plots.acoustic.plot_acoustic_pressure_field import PlotAcousticPressureField
from pulse.interface.user_input.plots.acoustic.plot_acoustic_frequency_response import PlotAcousticFrequencyResponse
from pulse.interface.user_input.plots.acoustic.plot_acoustic_frequency_response_function import PlotAcousticFrequencyResponseFunction
from pulse.interface.user_input.plots.acoustic.plot_transmission_loss import PlotTransmissionLoss
from pulse.interface.user_input.plots.acoustic.plot_acoustic_delta_pressure import PlotAcousticDeltaPressure
from pulse.interface.user_input.plots.acoustic.plotPerforatedPlateConvergenceData import PlotPerforatedPlateConvergenceData
#
from pulse.interface.user_input.plots.structural.plot_cross_section_input import PlotCrossSectionInput
from pulse.interface.user_input.project.render.renderer_user_preferences import RendererUserPreferencesInput
from pulse.interface.user_input.model.info.structural_model_info import StructuralModelInfo
from pulse.interface.user_input.model.info.acoustic_model_Info import AcousticModelInfo
from pulse.interface.user_input.model.criteria.check_beam_criteria_input import CheckBeamCriteriaInput
#
from pulse.interface.user_input.project.print_message import PrintMessageInput
#
from pulse.interface.user_input.render.section_plane_widget import SectionPlaneWidget
#
from pulse import app

from time import time

window_title_1 = "Error"
window_title_2 = "Warning"

class InputUi:
    def __init__(self, parent=None):

        self.main_window = app().main_window
        self.project = app().main_window.project
        self.file = app().project.file

        self.menu_items = app().main_window.model_and_analysis_setup_widget.model_and_analysis_setup_items

        self._reset()

    def _reset(self):
        self.analysis_id = None
        self.project.none_project_action = False

    def process_input(self, workingClass, *args, **kwargs):
        # try:
        app().main_window.close_dialogs()
        read = workingClass(*args, **kwargs)
        return read
        # except Exception as log_error:
        #     title = "Error detected in 'process_input' method"
        #     message = str(log_error)
        #     PrintMessageInput([window_title_1, title, message])
        #     return None

    def call_geometry_editor(self):
        main_window = self.main_window
        main_window.use_geometry_workspace()

    def set_material(self):
        self.process_input(SetMaterialInput)   

    def set_cross_section(self, pipe_to_beam=False, beam_to_pipe=False, lines_to_update_cross_section=[]):
        read = self.process_input(   SetCrossSectionInput,
                                    pipe_to_beam = pipe_to_beam, 
                                    beam_to_pipe = beam_to_pipe, 
                                    lines_to_update_cross_section = lines_to_update_cross_section   ) 
        return read.complete

    def set_structural_element_type(self):
        read = self.process_input(StructuralElementTypeInput)
        if read.complete:
            if read.pipe_to_beam or read.beam_to_pipe:         
                self.set_cross_section( pipe_to_beam = read.pipe_to_beam, 
                                        beam_to_pipe = read.beam_to_pipe, 
                                        lines_to_update_cross_section = read.list_lines_to_update_cross_section )

    def plot_cross_section(self):
        self.process_input(PlotCrossSectionInput)

    def mesh_setup_visibility(self):
        self.process_input(RendererUserPreferencesInput)

    def set_beam_xaxis_rotation(self):
        self.process_input(BeamXaxisRotationInput)

    def set_prescribed_dofs(self):
        self.process_input(PrescribedDofsInput)

    def set_rotation_decoupling_dofs(self):
        self.process_input(DecouplingRotationDOFsInput)

    def set_nodal_loads(self):
        self.process_input(NodalLoadsInput)

    def add_mass_spring_damper(self):
        self.process_input(MassSpringDamperInput)

    def set_capped_end(self):
        self.process_input(CappedEndInput)

    def set_stress_stress_stiffening(self):
        self.process_input(StressStiffeningInput)

    def add_elastic_nodal_links(self):
        self.process_input(ElasticNodalLinksInput)

    def set_inertial_load(self):
        return self.process_input(SetInertialLoad)

    def add_expansion_joint(self):
        self.process_input(ExpansionJointInput)

    def add_valve(self):
        return self.process_input(ValvesInput)

    def add_flanges(self):
        self.process_input(ConnectingFlangesInput)

    def set_acoustic_element_type(self):
        self.process_input(AcousticElementTypeInput)

    def set_fluid(self):
        self.process_input(SetFluidInput)

    def set_fluid_composition(self):
        self.process_input(SetFluidCompositionInput)

    def set_acoustic_pressure(self):
        self.process_input(AcousticPressureInput)

    def set_volume_velocity(self):
        self.process_input(VolumeVelocityInput)

    def set_specific_impedance(self):
        self.process_input(SpecificImpedanceInput)

    def set_radiation_impedance(self):
        self.process_input(RadiationImpedanceInput)

    def add_perforated_plate(self):
        self.process_input(PerforatedPlateInput)

    def set_acoustic_element_length_correction(self):
        self.process_input(AcousticElementLengthCorrectionInput)

    def add_compressor_excitation(self):
        self.process_input(CompressorModelInput)

    def pulsation_suppression_device_editor(self):
        self.process_input(PulsationSuppressionDeviceInput)

    def analysis_type_input(self):

        read = self.process_input(AnalysisTypeInput)

        if not read.complete:
            return

        if read.method_ID == -1:
            return

        self.analysis_id = self.project.analysis_id
        self.analysis_type_label = self.project.analysis_type_label
        self.analysis_method_label = self.project.analysis_method_label

        if self.analysis_id is None:
            self.analysis_id = None
            return
        
        if self.analysis_id in [0, 1, 3, 5, 6, 7]:
            self.project.set_structural_solution(None)
            self.project.set_acoustic_solution(None)

        if self.analysis_id in [2, 4, 7]:
            self.project.update_project_analysis_setup_state(True)
            self.run_analysis()
        else:
            self.analysis_setup()
                    
    def analysis_setup(self):

        if self.project.analysis_id in [None, 2, 4]:
            return False
        
        read = self.process_input(AnalysisSetupInput)
        
        if read.complete:
            if read.flag_run:
                self.run_analysis()
            return True   
        else:
            return False
       
    def run_analysis(self):

        # t0 = time()
        if self.analysis_id is None or not self.project.setup_analysis_complete:

            title = "INCOMPLETE SETUP ANALYSIS" 
            message = "Please, it is necessary to choose an analysis type and "
            message += "setup it before trying to solve the model."
            PrintMessageInput([window_title_1, title, message])
            return

        self.before_run = self.project.get_pre_solution_model_checks()
        if self.before_run.check_is_there_a_problem(self.analysis_id):
            return
        # self.project.time_to_checking_entries = time()-t0

        read = self.process_input(RunAnalysisInput)
        if read.complete:
            if self.analysis_id == 2:
                self.before_run.check_modal_analysis_imported_data()
            elif self.analysis_id in [3, 5, 6]:
                self.before_run.check_all_acoustic_criteria()

            self.after_run = self.project.get_post_solution_model_checks()
            self.after_run.check_all_acoustic_criterias()
            self.main_window.use_results_workspace()
            app().main_window.results_widget.show_empty()
        
    def plot_structural_mode_shapes(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = False
        self.project.plot_stress_field = False
        solution = self.project.get_structural_solution()
        if self.analysis_id in [2, 4]:
            if solution is None:
                return None
            else:
                return self.process_input(PlotStructuralModeShape)      

    def plot_displacement_field(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = False
        self.project.plot_stress_field = False
        solution = self.project.get_structural_solution()
        if self.analysis_id in [0, 1, 5, 6, 7]:
            if solution is None:
                return None
            else:
                return self.process_input(PlotNodalResultsFieldForHarmonicAnalysis)

    def plot_structural_frequency_response(self):
        if self.analysis_id in [0, 1, 5, 6, 7]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return None
            elif self.analysis_id == 7:
                return self.process_input(PlotNodalResultsForStaticAnalysis)
            else:
                return self.process_input(PlotNodalResultsForHarmonicAnalysis)

    def plot_reaction_frequency_response(self):
        if self.analysis_id in [0, 1, 5, 6]:
            return self.process_input(PlotReactionsForHarmonicAnalysis)
        elif self.analysis_id == 7:
            return self.process_input(PlotReactionsForStaticAnalysis)  

    def plot_stress_field(self):
        self.project.plot_pressure_field = False
        self.project.plot_stress_field = True
        if self.analysis_id in [0, 1, 5, 6, 7]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return
            elif self.analysis_id == 7:
                return self.process_input(PlotStressesFieldForStaticAnalysis)
            else:
                return self.process_input(PlotStressesFieldForHarmonicAnalysis)

    def plot_stress_frequency_response(self):
        solution = self.project.get_structural_solution()
        if self.analysis_id in [0, 1, 5, 6, 7]:
            if solution is None:
                return
            elif self.analysis_id == 7:
                return self.process_input(PlotStressesForStaticAnalysis)
            else:
                return self.process_input(PlotStressesForHarmonicAnalysis)     

    def plot_acoustic_mode_shapes(self):
        self.project.plot_pressure_field = True
        self.project.plot_stress_field = False
        solution = self.project.get_acoustic_solution()
        if self.analysis_id in [2, 4]:
            if solution is None:
                return None
            else:
                return self.process_input(PlotAcousticModeShape)           

    def plot_acoustic_pressure_field(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = True
        self.project.plot_stress_field = False
        solution = self.project.get_acoustic_solution()
        if self.analysis_id in [3, 5, 6]:
            if solution is None:
                return None
            else:
                return self.process_input(PlotAcousticPressureField)

    def plot_acoustic_frequency_response(self):
        if self.analysis_id in [3, 5, 6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return None
            else:
                return self.process_input(PlotAcousticFrequencyResponse)

    def plot_acoustic_frequency_response_function(self):
        if self.analysis_id in [3, 5, 6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return None
            else:
                return self.process_input(PlotAcousticFrequencyResponseFunction)

    def plot_acoustic_delta_pressures(self):
        if self.analysis_id in [3, 5, 6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return None
            else:
                return self.process_input(PlotAcousticDeltaPressure)

    def plot_transmission_loss(self):
        if self.analysis_id in [3, 5, 6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return None
            else:
                return self.process_input(PlotTransmissionLoss)

    def plot_perforated_plate_convergence_data(self):
        if self.project.perforated_plate_data_log:
            self.process_input(PlotPerforatedPlateConvergenceData)
    
    def check_api618_pulsation_criteria(self):
        return self.process_input(CheckAPI618PulsationCriteriaInput)

    def shaking_forces_criteria(self):
        return self.process_input(ShakingForcesCriteriaInput)

    def structural_model_info(self):
        self.process_input(StructuralModelInfo)

    def acoustic_model_info(self):
        self.process_input(AcousticModelInfo)

    def check_beam_criteria(self):
        self.process_input(CheckBeamCriteriaInput)

    def geometry_editor_help(self):
        self.process_input(GeometryEditorHelp)

    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = "Please, you should create a new project or load an already existing one before start to set up the model. "
        message += "It is recommended to use the 'New Project' or the 'Import Project' buttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([window_title, title, message])