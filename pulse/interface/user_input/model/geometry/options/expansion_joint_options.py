from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget


from copy import deepcopy

from opps.model import ExpansionJoint

from molde.stylesheets import set_qproperty

from .structure_options import StructureOptions

from pulse import app
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.model.setup.structural.expansion_joint_input import ExpansionJointInput

window_title = "Error"

class ExpansionJointOptions(StructureOptions):
    def __init__(self, geometry_designer_widget: "GeometryDesignerWidget") -> None:
        super().__init__()

        self.geometry_designer_widget = geometry_designer_widget
        self.cross_section_widget = self.geometry_designer_widget.cross_section_widget

        self.structure_type = ExpansionJoint
        self.expansion_joint_info = dict()
        self.update_permissions()
    
    def xyz_callback(self, xyz):
        kwargs = self._get_kwargs()
        if kwargs is None:
            return

        self.pipeline.dismiss()
        self.pipeline.clear_structure_selection()
        self.pipeline.add_expansion_joint(xyz, **kwargs)

    def attach_callback(self):
        kwargs = self._get_kwargs()
        if kwargs is None:
            return
        self.pipeline.connect_expansion_joints(**kwargs)

    def configure_structure(self):
        app().main_window.close_dialogs()
        self.expansion_joint_input = ExpansionJointInput(render_type="geometry")
        self.load_data_from_pipe_section()
        self.expansion_joint_input.exec_callback()
        app().main_window.set_input_widget(None)

        if not self.expansion_joint_input.complete:
            self.expansion_joint_info = None
            return

        self.expansion_joint_info = self.expansion_joint_input.expansion_joint_info
        self.configure_section_of_selected()
        self.update_permissions()

    def update_permissions(self):
        if self.expansion_joint_info:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=False, status="default")
            enable = True
        else:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=True, status="danger")
            enable = False

        enable_attach = len(self.pipeline.selected_points) >= 2
        enable_add = len(self.pipeline.staged_structures) + len(self.pipeline.staged_points) >= 1
        enable_delete = len(self.pipeline.selected_structures) + len(self.pipeline.selected_points) >= 1

        self.geometry_designer_widget.configure_button.setEnabled(True)
        self.geometry_designer_widget.frame_bounding_box_sizes.setEnabled(enable)
        self.geometry_designer_widget.attach_button.setEnabled(enable_attach)
        self.geometry_designer_widget.add_button.setEnabled(enable_add)
        self.geometry_designer_widget.delete_button.setEnabled(enable_delete)

    def load_data_from_pipe_section(self):

        outside_diameter = self.cross_section_widget.lineEdit_outside_diameter.text()
        wall_thickness = self.cross_section_widget.lineEdit_wall_thickness.text()

        try:

            section_parameters = self.cross_section_widget.pipe_section_info["section_parameters"]
            outside_diameter = section_parameters[0]
            wall_thickness = section_parameters[1]
            effective_diameter = outside_diameter - 2 * wall_thickness

            self.expansion_joint_input.lineEdit_effective_diameter.setText(f"{round(effective_diameter, 6)}")
            # self.expansion_joint_input.lineEdit_wall_thickness.setText(f"{round(wall_thickness, 6)}")
        
        except Exception as error_log:
            title = "Error while tranfering pipe data"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])

    def _get_kwargs(self) -> dict:
        if self.expansion_joint_info is None:
            return

        return dict(
            diameter = self.expansion_joint_info.get("effective_diameter", 0),
            thickness = 0,
            extra_info = self._get_extra_info(),
        )

    def _get_extra_info(self):
        return dict(
            structural_element_type = "expansion_joint",
            expansion_joint_info = deepcopy(self.expansion_joint_info),
            material_info = self.geometry_designer_widget.current_material_info,
        )
