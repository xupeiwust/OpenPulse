from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget


from copy import deepcopy

from opps.model import RectangularBeam

from molde.stylesheets import set_qproperty

from .structure_options import StructureOptions
from pulse import app


class RectangularBeamOptions(StructureOptions):
    def __init__(self, geometry_designer_widget: "GeometryDesignerWidget") -> None:
        super().__init__()

        self.geometry_designer_widget = geometry_designer_widget
        self.cross_section_widget = self.geometry_designer_widget.cross_section_widget

        self.structure_type = RectangularBeam
        self.cross_section_info: dict = self.cross_section_widget.beam_section_info
        self.update_permissions()
    
    def xyz_callback(self, xyz):
        if self.cross_section_info is None:
            return

        parameters = self.cross_section_info.get("section_parameters")
        if parameters is None:
            return
        
        self.pipeline.dismiss()
        self.pipeline.clear_structure_selection()
        self.pipeline.add_rectangular_beam(
            xyz,
            width = parameters[0],
            height = parameters[1],
            thickness = (parameters[0] - parameters[2]) / 2,
            extra_info = self._get_extra_info(),
        )

    def attach_callback(self):
        if self.cross_section_info is None:
            return

        parameters = self.cross_section_info.get("section_parameters")
        if parameters is None:
            return

        self.pipeline.connect_rectangular_beams(
            width = parameters[0],
            height = parameters[1],
            thickness = (parameters[0] - parameters[2]) / 2,
            extra_info = self._get_extra_info(),
        )

    def configure_structure(self):
        self.cross_section_widget.set_inputs_to_geometry_creator()     
        self.cross_section_widget.hide_all_tabs()     
        self.cross_section_widget.tabWidget_general.setTabVisible(1, True)
        self.cross_section_widget.tabWidget_beam_section.setTabVisible(0, True)
        self.cross_section_widget.lineEdit_height_C_section.setFocus()
        self.cross_section_widget.exec()

        if not self.cross_section_widget.complete:
            return
        
        if self.cross_section_widget.get_beam_section_parameters():
            self.configure_structure()  # if it is invalid try again
            return

        self.cross_section_info = self.cross_section_widget.beam_section_info
        self.update_permissions()

    def update_permissions(self):
        if self.cross_section_info:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=False, status="default")
            enable = True
        else:
            set_qproperty(self.geometry_designer_widget.configure_button, warning=True, status="danger")
            enable = False

        self.geometry_designer_widget.create_structure_frame.setEnabled(enable)

    def _get_extra_info(self):
        return dict(
            structural_element_type = "beam_1",
            cross_section_info = deepcopy(self.cross_section_info),
            current_material_info = self.geometry_designer_widget.current_material_info,
        )
