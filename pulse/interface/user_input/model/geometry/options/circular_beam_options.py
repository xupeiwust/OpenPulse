from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget


from copy import deepcopy

from pulse.editor.structures import CircularBeam

from molde.stylesheets import set_qproperty

from .structure_options import StructureOptions
from pulse import app


class CircularBeamOptions(StructureOptions):
    structure_type = CircularBeam

    def get_kwargs(self) -> dict:
        if self.structure_info is None:
            return

        parameters = self.structure_info.get("section_parameters")
        if parameters is None:
            return

        return dict(
            diameter = parameters[0],
            thickness = parameters[1],
            extra_info = self._get_extra_info(),
        )

    def configure_structure(self):
        self.cross_section_widget._add_icon_and_title()
        self.cross_section_widget.set_inputs_to_geometry_creator()     
        self.cross_section_widget.hide_all_tabs()     
        self.cross_section_widget.tabWidget_general.setTabVisible(1, True)
        self.cross_section_widget.tabWidget_beam_section.setTabVisible(1, True)
        self.cross_section_widget.lineEdit_outside_diameter_circular_section.setFocus()
        self.cross_section_widget.exec()

        if not self.cross_section_widget.complete:
            return
        
        if self.cross_section_widget.get_beam_section_parameters():
            self.configure_structure()  # if it is invalid try again
            return

        self.structure_info = self.cross_section_widget.beam_section_info
        self.configure_section_of_selected()
        self.update_permissions()

    def update_permissions(self):
        if self.structure_info:
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

    def _get_extra_info(self):
        return dict(
            structural_element_type = "beam_1",
            cross_section_info = deepcopy(self.structure_info),
            material_info = self.geometry_designer_widget.current_material_info,
        )
