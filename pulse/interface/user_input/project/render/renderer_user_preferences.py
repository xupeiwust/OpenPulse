from PyQt5.QtWidgets import QDialog, QCheckBox, QFrame, QLineEdit, QPushButton, QRadioButton, QSlider, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.model.setup.general.color_selector import PickColorInput
from pulse.interface.viewer_3d.renders.opvRenderer import PlotFilter, SelectionFilter


class RendererUserPreferencesInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(UI_DIR / "project/render/renderer_user_preferences.ui", self)

        self.main_window = app().main_window
        self.config = app().config
        self.project = app().project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._load_logo_state()
        self._load_reference_scale_state()
        self._load_color_state()
        # self.load_plot_state()
        # self.load_selection_state()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)

    def _initialize(self):
        self.cache_setup = [self.opv.background_color,
                            self.opv.font_color,
                            self.opv.opvRenderer.nodes_color,
                            self.opv.opvRenderer.lines_color,
                            self.opv.opvRenderer.surfaces_color,
                            self.opv.opvRenderer.elements_transparency]

    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_OpenPulse_logo : QCheckBox
        self.checkBox_MOPT_logo : QCheckBox
        self.checkBox_reference_scale : QCheckBox
        self.checkBox_background_color : QCheckBox
        # QFrame
        self.frame_background_color : QFrame
        # QSlider
        self.slider_transparency : QSlider
        # QLineEdit
        self.lineEdit_background_color : QLineEdit
        self.lineEdit_font_color : QLineEdit
        self.lineEdit_nodes_color : QLineEdit
        self.lineEdit_lines_color : QLineEdit
        self.lineEdit_surfaces_color : QLineEdit
        self.lineEdit_elements_transparency : QLineEdit
        # QPushButton
        self.pushButton_background_color : QPushButton
        self.pushButton_font_color : QPushButton
        self.pushButton_nodes_color : QPushButton
        self.pushButton_lines_color : QPushButton
        self.pushButton_surfaces_color : QPushButton
        self.pushButton_update_settings : QPushButton
        # QRadioButton
        self.radioButton_black_color : QRadioButton
        self.radioButton_dark_gray_color : QRadioButton
        self.radioButton_light_gray_color : QRadioButton
        self.radioButton_white_color : QRadioButton
        # QTabWidget
        self.tabWidget_main : QTabWidget

    def _create_connections(self):
        self.checkBox_background_color.stateChanged.connect(self.update_background_color_controls_visibility)
        self.pushButton_background_color.clicked.connect(self.update_background_color)
        self.pushButton_font_color.clicked.connect(self.update_font_color)
        self.pushButton_nodes_color.clicked.connect(self.update_nodes_color)
        self.pushButton_lines_color.clicked.connect(self.update_lines_color)
        self.pushButton_surfaces_color.clicked.connect(self.update_surfaces_color)
        self.slider_transparency.valueChanged.connect(self.update_transparency_value)
        self.pushButton_update_settings.clicked.connect(self.confirm_and_update_user_preferences)
        self.update_slider_transparency()

    def update_background_color_controls_visibility(self):
        _bool = self.checkBox_background_color.isChecked()
        self.pushButton_background_color.setDisabled(not _bool)
        self.lineEdit_background_color.setDisabled(not _bool)

    def _load_reference_scale_state(self):
        self.checkBox_reference_scale.setChecked(self.opv.show_reference_scale)

    def _load_color_state(self):

        self.background_color = self.opv.background_color
        self.font_color = self.opv.font_color
        self.nodes_color = self.opv.opvRenderer.nodes_color
        self.lines_color = self.opv.opvRenderer.lines_color
        self.surfaces_color = self.opv.opvRenderer.surfaces_color
        self.elements_transparency = self.opv.opvRenderer.elements_transparency

        if self.background_color is None:
            self.checkBox_background_color.setChecked(False)
            self.pushButton_background_color.setDisabled(True)
            self.lineEdit_background_color.setDisabled(True)
        else:
            self.checkBox_background_color.setChecked(True)
            self.pushButton_background_color.setDisabled(False)
            self.lineEdit_background_color.setDisabled(False)
            str_color = str(self.background_color)[1:-1]
            self.lineEdit_background_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

        str_color = str(self.font_color)[1:-1]
        self.lineEdit_font_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

        str_color = str(self.nodes_color)[1:-1]
        self.lineEdit_nodes_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

        str_color = str(self.lines_color)[1:-1]
        self.lineEdit_lines_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

        str_color = str(self.surfaces_color)[1:-1]
        self.lineEdit_surfaces_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
    
    def _load_logo_state(self):
        self.checkBox_OpenPulse_logo.setChecked(self.opv.add_OpenPulse_logo)
        self.checkBox_MOPT_logo.setChecked(self.opv.add_MOPT_logo)

    def update_background_color_state(self):
        self.opv.background_color = self.background_color
        self.opv.opvRenderer.set_background_color(self.background_color)
        self.opv.opvAnalysisRenderer.set_background_color(self.background_color)

    def update_font_color_state(self):
        self.opv.font_color = self.font_color
        self.opv.opvRenderer.changeFontColor(self.font_color)
        self.opv.opvAnalysisRenderer.changeFontColor(self.font_color)
        self.opv.opvRenderer._updateFontColor(self.font_color)
        self.opv.opvAnalysisRenderer._updateFontColor(self.font_color)
    
    def update_reference_scale_state(self):
        self.opv.show_reference_scale = self.checkBox_reference_scale.isChecked()
        self.opv.opvRenderer._createScaleBar()
        self.opv.opvAnalysisRenderer._createScaleBar()
            
    def update_logo_state(self):     
        self.opv.add_OpenPulse_logo = self.checkBox_OpenPulse_logo.isChecked()
        self.opv.add_MOPT_logo = self.checkBox_MOPT_logo.isChecked()
        self.opv.opvRenderer._createLogos(OpenPulse=self.opv.add_OpenPulse_logo, MOPT=self.opv.add_MOPT_logo)
        self.opv.opvAnalysisRenderer._createLogos(OpenPulse=self.opv.add_OpenPulse_logo, MOPT=self.opv.add_MOPT_logo)

    def update_transparency_value(self):
        self.elements_transparency = (self.slider_transparency.value()/100)
        self.lineEdit_elements_transparency.setText(str(self.elements_transparency))

    def update_slider_transparency(self):
        value = self.opv.opvRenderer.elements_transparency
        self.slider_transparency.setValue(int(100*value))
        self.lineEdit_elements_transparency.setText(str(value))

    def update_background_color(self):
        read = PickColorInput(title="Pick the background color")
        if read.complete:
            self.background_color = tuple(read.color)
            str_color = str(self.background_color)[1:-1]
            self.lineEdit_background_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
            return False
        return True

    def update_font_color(self):
        read = PickColorInput(title="Pick the font color")
        if read.complete:
            self.font_color = tuple(read.color)
            str_color = str(self.font_color)[1:-1]
            self.lineEdit_font_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
        else:
            return

    def update_nodes_color(self):
        read = PickColorInput(title="Pick the nodes color")
        if read.complete:
            self.nodes_color = tuple(read.color)
            str_color = str(self.nodes_color)[1:-1]
            self.lineEdit_nodes_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
        else:
            return 
        
    def update_lines_color(self):
        read = PickColorInput(title="Pick the lines color")
        if read.complete:
            self.lines_color = tuple(read.color)
            str_color = str(self.lines_color)[1:-1]
            self.lineEdit_lines_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
        else:
            return

    def update_surfaces_color(self):
        read = PickColorInput(title="Pick the surfaces color")
        if read.complete:
            self.surfaces_color = tuple(read.color)
            str_color = str(self.surfaces_color)[1:-1]
            self.lineEdit_surfaces_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
        else:
            return        

    def update_nodes_lines_elements_settings(self):
        self.opv.opvRenderer.changeNodesColor(self.nodes_color)
        self.opv.opvRenderer.changeLinesColor(self.lines_color)
        self.opv.opvRenderer.changeSurfacesColor(self.surfaces_color)
        self.opv.opvRenderer.changeElementsTransparency(self.elements_transparency)

    def confirm_and_update_user_preferences(self):

        self.update_logo_state()

        if self.checkBox_background_color.isChecked():
            if self.background_color is None:
                if self.update_background_color():
                    return
                self.update_background_color_state()

        self.update_font_color_state()
        self.update_reference_scale_state()
        self.update_nodes_lines_elements_settings()
        self.update_transparency_value()

        preferences = { 'interface theme' : self.main_window.interface_theme,
                        'render theme' : self.opv.render_theme,
                        'background color' : str(self.opv.background_color),
                        'font color' : str(self.opv.font_color),
                        'nodes color' : str(self.opv.opvRenderer.nodes_color),
                        'lines color' : str(self.opv.opvRenderer.lines_color),
                        'surfaces color' : str(self.opv.opvRenderer.surfaces_color),
                        'transparency' : str(self.opv.opvRenderer.elements_transparency),
                        'OpenPulse logo' : str(int(self.opv.add_OpenPulse_logo)),
                        'mopt logo' : str(int(self.opv.add_MOPT_logo)),
                        'Reference scale' : str(int(self.opv.show_reference_scale)) }
        
        self.config.write_user_preferences_in_file(preferences)
        # self.project.elements_transparency = self.transparency
        
        self.update_renders()
        self.close()

    def update_renders(self):

        final_setup = [ self.opv.background_color,
                        self.opv.font_color,
                        self.opv.opvRenderer.nodes_color,
                        self.opv.opvRenderer.lines_color,
                        self.opv.opvRenderer.surfaces_color,
                        self.opv.opvRenderer.elements_transparency ]

        if final_setup != self.cache_setup:
            self.opv.updateRendererMesh()
            self.main_window.update_plot_mesh()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_and_update_user_preferences()
        elif event.key() == Qt.Key_Escape:
            self.close()