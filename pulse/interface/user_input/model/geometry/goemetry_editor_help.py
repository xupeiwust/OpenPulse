from PyQt5.QtWidgets import QDialog, QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

class GeometryEditorHelp(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(UI_DIR / "help/geometry_editor_help.ui", self)

        self.main_window = app().main_window
        self.project = app().project
        self.file = self.project.file

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.exec()

    def _initialize(self):
        pass

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Quick manual")
        self.setWindowIcon(self.icon)

    def _define_qt_variables(self):
        self.pushButton_close : QPushButton
        self.pushButton_tutorial : QPushButton

    def _create_connections(self):
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_tutorial.clicked.connect(self.show_tutorial)

    def show_tutorial(self):
        pass