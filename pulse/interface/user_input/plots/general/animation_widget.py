from PyQt5.QtWidgets import QFrame, QCheckBox, QLabel, QLineEdit, QPushButton, QSlider, QSpinBox, QWidget
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt, QEvent
from PyQt5 import uic

from pathlib import Path
import os

from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.tools.utils import get_new_path
from pulse import app, UI_DIR

window_title_1 = "Error"
window_title_2 = "Warning"


class AnimationWidget(QWidget):
    def __init__(self):
        super().__init__()

        ui_path = Path(f"{UI_DIR}/plots/animation/animation_widget.ui")
        uic.loadUi(ui_path, self)

        main_window = app().main_window
        self.main_window = main_window

        self._define_qt_variables()
        self._create_connections()

    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_export = self.findChild(QCheckBox, 'checkBox_export')
        # QLabel
        self.label_export_path = self.findChild(QLabel, 'label_export_path')
        # QLineEdit
        self.lineEdit_file_name = self.findChild(QLineEdit, 'lineEdit_file_name')      
        # QPushButton
        self.pushButton_animate = self.findChild(QPushButton, "pushButton_animate")
        # QSlider
        self.phase_slider = self.findChild(QSlider, "phase_slider")
        # QSpinBox
        self.spinBox_frames = self.findChild(QSpinBox, 'spinBox_frames')
        self.spinBox_cycles = self.findChild(QSpinBox, 'spinBox_cycles')

    def _create_connections(self):
        self.phase_slider.valueChanged.connect(self.slider_callback)
        self.pushButton_animate.clicked.connect(self.process_animation)
        self.spinBox_frames.valueChanged.connect(self.frames_value_changed)
        self.spinBox_cycles.valueChanged.connect(self.cycles_value_changed)

    def frames_value_changed(self):
        self.main_window.opv_widget.opvAnalysisRenderer._numberFramesHasChanged(True)
        self.frames = self.spinBox_frames.value()
        
    def cycles_value_changed(self):
        self.cycles = self.spinBox_cycles.value()

    def slider_callback(self):
        value = self.phase_slider.value()
        self.main_window.opv_widget.opvAnalysisRenderer.slider_callback(value)

    def process_animation(self):
        self.update_animation_settings()
        self.main_window.opv_widget.opvAnalysisRenderer._setNumberFrames(self.frames)
        self.main_window.opv_widget.opvAnalysisRenderer._setNumberCycles(self.cycles)
        # self.main_window.opv_widget.opvAnalysisRenderer.playAnimation()
        self.main_window.opv_widget.opvAnalysisRenderer.tooglePlayPauseAnimation()

    def update_animation_settings(self):
        self.frames = self.spinBox_frames.value()
        self.cycles = self.spinBox_cycles.value()

    def get_file_format(self):
        index = self.comboBox_file_format.currentIndex()
        _formats = [".mp4", ".ogv", ".mpeg", ".avi"]
        return _formats[index]

    def export_animation_to_file(self):
        if self.lineEdit_file_name.text() != "":
            file_format = self.get_file_format()
            filename = self.lineEdit_file_name.text() + file_format
            if os.path.exists(self.save_path):
                self.export_file_path = get_new_path(self.save_path, filename)
                self.update_animation_settings()
                self.opv.opvAnalysisRenderer.start_export_animation_to_file(self.export_file_path, self.frames)
                self.process_animation()
            else:
                title = "Invalid folder path"
                message = "Inform a valid folder path before trying export the animation.\n\n"
                message += f"{self.label_export_path.text()}"
                PrintMessageInput([window_title_1, title, message])
                self.label_export_path.setText("<Folder path>")
        else:
            title = "Empty file name"
            message = "Inform a file name before trying export the animation."
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_file_name.setFocus()