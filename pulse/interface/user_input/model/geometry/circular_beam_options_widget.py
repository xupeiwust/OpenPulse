from copy import deepcopy

from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QLabel, QStackedWidget, QTabWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

from opps.model import CircularBeam

from pulse import app, UI_DIR
from pulse.interface.user_input.model.setup.cross_section.cross_section_inputs import CrossSectionWidget


class CircularBeamOptionsWidget(QWidget):
    edited = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        ui_path = UI_DIR / "model/geometry/rectangular_beam_option_widget.ui"
        uic.loadUi(ui_path, self)

        self.pipeline = app().project.pipeline

        self.structure_type = CircularBeam
        self.add_function = self.pipeline.add_circular_beam
        self.attach_function = self.pipeline.connect_circular_beams
        self.cross_section_info = None

        self._define_qt_variables()
        self._create_layout()
        self._create_connections()
        self._initialize()

    def _define_qt_variables(self):
        self.set_section_button: QPushButton
        self.cross_section_widget = CrossSectionWidget(self)

    def _create_layout(self):
        self.cross_section_widget._add_icon_and_title()
        self.cross_section_widget.set_inputs_to_geometry_creator()     
        self.cross_section_widget.hide_all_tabs()     
        self.cross_section_widget.tabWidget_general.setTabVisible(1, True)
        self.cross_section_widget.tabWidget_beam_section.setTabVisible(1, True)
        self.cross_section_widget.lineEdit_outside_diameter_circular_section.setFocus()
        self.cross_section_widget.hide()

    def _create_connections(self):
        self.set_section_button.clicked.connect(self.show_cross_section_widget_callback)
        self.cross_section_widget.pushButton_confirm_beam.clicked.connect(self.define_cross_section_callback)

    def _initialize(self):
        self.set_section_button.setProperty("warning", True)
        self.style().polish(self.set_section_button)

    def get_parameters(self) -> dict:
        if self.cross_section_info is None:
            return

        parameters = self.cross_section_info.get("section_parameters")
        if parameters is None:
            return

        kwargs = dict()
        kwargs["diameter"] = parameters[0]
        kwargs["thickness"] = parameters[1]
        kwargs["extra_info"] = dict(
            structural_element_type = "beam_1",
            cross_section_info = deepcopy(self.cross_section_info),
        )
        return kwargs

    def show_cross_section_widget_callback(self):
        self.cross_section_widget.show()

    def define_cross_section_callback(self):
        if self.cross_section_widget.get_beam_section_parameters():
            return

        self.cross_section_info = self.cross_section_widget.beam_section_info
        self.cross_section_widget.hide()
        self.set_section_button.setProperty("warning", False)
        self.style().polish(self.set_section_button)
        self.edited.emit()
