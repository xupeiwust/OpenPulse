from copy import deepcopy
import warnings

from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QLabel, QStackedWidget, QTabWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

from opps.model import ExpansionJoint

from pulse import app, UI_DIR
from pulse.interface.utils import set_qt_property
from pulse.interface.user_input.model.setup.cross_section.cross_section_widget import CrossSectionWidget
from pulse.interface.user_input.model.setup.structural.expansion_joint_geometry_input import ExpansionJointGeometryInput


class ExpansionJointOptionsWidget(QWidget):
    edited = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        ui_path = UI_DIR / "model/geometry/expansion_joint_option_widget.ui"
        uic.loadUi(ui_path, self)

        self.pipeline = app().project.pipeline
        self.structure_type = ExpansionJoint
        self.add_function = self.pipeline.add_expansion_joint
        self.attach_function = self.pipeline.connect_expansion_joints
        self.cross_section_info = None
        self.expansion_joint_info = None

        self._initialize()
        self._define_qt_variables()
        self._create_connections()

    def _initialize(self):
        self.set_section_button.setProperty("warning", True)
        self.style().polish(self.set_section_button)

    def _define_qt_variables(self):
        self.set_section_button: QPushButton
        self.cross_section_widget: CrossSectionWidget = self.parent().cross_section_widget

    def _config_layout(self):
        self.cross_section_widget._add_icon_and_title()
        self.cross_section_widget.set_inputs_to_geometry_creator()     
        self.cross_section_widget.hide_all_tabs()     
        self.cross_section_widget.tabWidget_general.setTabVisible(0, True)
        self.cross_section_widget.tabWidget_pipe_section.setTabVisible(0, True)
        self.cross_section_widget.lineEdit_outside_diameter.setFocus()
        self.cross_section_widget.hide()

    def _create_connections(self):
        self.set_section_button.clicked.connect(self.define_cross_section_callback)

    def get_parameters(self) -> dict:
        if self.expansion_joint_info is None:
            return

        kwargs = dict()
        kwargs["diameter"] = self.expansion_joint_info["effective_diameter"]
        kwargs["thickness"] = 0
        kwargs["extra_info"] = dict(
            structural_element_type = "pipe_1",
            expansion_joint_parameters = deepcopy(self.expansion_joint_info),
        )
        return kwargs

    def define_cross_section_callback(self):
        geometry_input = ExpansionJointGeometryInput()
        self.expansion_joint_info = geometry_input.value
        if self.expansion_joint_info is None:
            return

        set_qt_property(self.set_section_button, warning=False)
        self.edited.emit()
