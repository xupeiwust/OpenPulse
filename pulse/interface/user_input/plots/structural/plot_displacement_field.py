from PyQt5.QtWidgets import QComboBox, QFrame, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import numpy as np

from pulse import app
from pulse.interface.user_input.project.print_message import PrintMessageInput

class PlotDisplacementField(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        main_window = app().main_window

        ui_path = f"{main_window.ui_dir}/plots/results/structural/plot_displacement_field_for_harmonic_analysis.ui"
        uic.loadUi(ui_path, self)

        self.opv = main_window.getOPVWidget()
        self.opv.setInputObject(self)
        self.project = main_window.getProject()

        self._config_window()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.load_frequencies_vector()

    def _config_window(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon) 
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _reset_variables(self):
        self.frequencies = self.project.frequencies
        self.frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))
        self.frequency = None
        self.scaling_key = {0 : "absolute",
                            1 : "real_ux",
                            2 : "real_uy",
                            3 : "real_uz"}

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_color_scaling = self.findChild(QComboBox, 'comboBox_color_scaling')
        # QFrame
        self.frame_plot_button = self.findChild(QFrame, 'frame_plot_button')
        self.frame_plot_button.setVisible(False)
        # QLineEdit
        self.lineEdit_selected_frequency = self.findChild(QLineEdit, 'lineEdit_selected_frequency')
        # QPushButton
        self.pushButton_plot = self.findChild(QPushButton, 'pushButton_plot')
        # QTreeWidget
        self.treeWidget_frequencies = self.findChild(QTreeWidget, 'treeWidget_frequencies')
        self._config_treeWidget()

    def _create_connections(self):
        self.comboBox_color_scaling.currentIndexChanged.connect(self.update_plot)
        self.pushButton_plot.clicked.connect(self.update_plot)
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)

    def _config_treeWidget(self):
        widths = [80, 140]
        for i, width in enumerate(widths):
            self.treeWidget_frequencies.setColumnWidth(i, width)
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def update_plot(self):
        self.complete = False
        if self.lineEdit_selected_frequency.text() != "":
            if self.check_selected_frequency():
                self.complete = True

    def check_selected_frequency(self):
        if self.lineEdit_selected_frequency.text() == "":
            window_title = "Warning"
            title = "Additional action required to plot the results"
            message = "You should select a frequency from the available list "
            message += "before trying to plot the displacement/rotation field."
            PrintMessageInput([window_title, title, message], auto_close=True)
            return
        else:
            frequency_selected = float(self.lineEdit_selected_frequency.text())
            if frequency_selected in self.frequencies:
                self.frequency = self.frequency_to_index[frequency_selected]
                index = self.comboBox_color_scaling.currentIndex()
                current_scaling = self.scaling_key[index]
                self.opv.plot_displacement_field(self.frequency, current_scaling)

    def load_frequencies_vector(self):

        if self.project.analysis_ID == 7:
            self.plot_displacement_for_static_analysis()
            
        self.treeWidget_frequencies.clear()
        for index, frequency in enumerate(self.frequencies):
            new = QTreeWidgetItem([str(index+1), str(frequency)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)

    def plot_displacement_for_static_analysis(self):
        self.lineEdit_selected_frequency.setDisabled(True)
        self.treeWidget_frequencies.setDisabled(True)
        self.frequency = [0]
        self.lineEdit_selected_frequency.setText(str(self.frequency[0]))
        index = self.comboBox_color_scaling.currentIndex()
        current_scaling = self.scaling_key[index]
        self.opv.plot_displacement_field(self.frequency[0], current_scaling)

    def on_click_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.update_plot()

    def on_doubleclick_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.update_plot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()