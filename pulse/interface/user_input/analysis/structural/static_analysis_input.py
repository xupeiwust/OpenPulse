from PyQt5.QtWidgets import QDialog, QCheckBox, QPushButton
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.model.node import DOF_PER_NODE_STRUCTURAL


class StaticAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "analysis/structural/static_analysis.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.project = app().project
        self.model = app().project.model
        
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._load_current_state()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.complete = False

        # self.gravity = np.zeros(DOF_PER_NODE_STRUCTURAL, dtype=float)

        self.gravity_vector = app().project.model.gravity_vector


    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_self_weight_load : QCheckBox
        self.checkBox_internal_pressure_load : QCheckBox
        self.checkBox_external_nodal_loads : QCheckBox
        self.checkBox_distributed_element : QCheckBox

        # QPushButton
        self.pushButton_run_analysis : QPushButton

    def _create_connections(self):
        self.pushButton_run_analysis.clicked.connect(self.run_analysis_callback)

    def _load_current_state(self):
        self.checkBox_self_weight_load.setChecked(app().project.model.weight_load)
        self.checkBox_internal_pressure_load.setChecked(app().project.model.internal_pressure_load)
        self.checkBox_external_nodal_loads.setChecked(app().project.model.external_nodal_loads)
        self.checkBox_distributed_element.setChecked(app().project.model.element_distributed_load)

    def run_analysis_callback(self):

        weight_load = self.checkBox_self_weight_load.isChecked()
        internal_pressure_load = self.checkBox_internal_pressure_load.isChecked()
        external_nodal_load = self.checkBox_external_nodal_loads.isChecked()
        distributed_load = self.checkBox_distributed_element.isChecked()

        analysis_setup = { 
                           "f_min" : None,
                           "f_max" : None,
                           "f_step" : None,
                           "frequencies" : [0],
                           "damping_global" : [0, 0, 0, 0],
                           "weight_load" : weight_load,
                           "internal_pressure_load" : internal_pressure_load,
                           "external_pressure_load" : external_nodal_load,
                           "distributed_load" : distributed_load
                           }

        app().project.model.set_analysis_setup(analysis_setup)

        self.complete = True
        self.close()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm()
        elif event.key() == Qt.Key_Escape:
            self.close()