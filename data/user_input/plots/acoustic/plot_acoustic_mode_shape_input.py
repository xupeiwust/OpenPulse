from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import numpy as np

from data.user_input.project.printMessageInput import PrintMessageInput

window_title_1 = "ERROR MESSAGE"
window_title_2 = "WARNING MESSAGE"

class PlotAcousticModeShapeInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        uic.loadUi(Path('data/user_input/ui_files/plots_/results_/acoustic_/plot_acoustic_mode_shape_input.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)

        self.project = project
        self.natural_frequencies = project.natural_frequencies_acoustic
        self.mode_index = None

        self._define_qt_variables()
        self._create_connections()
        self.load_natural_frequencies()
        self.exec()


    def _define_qt_variables(self):
        # QLineEdit
        self.lineEdit_natural_frequency = self.findChild(QLineEdit, 'lineEdit_natural_frequency')
        self.lineEdit_natural_frequency.setDisabled(True)
        # QPushButton
        self.pushButton_plot = self.findChild(QPushButton, 'pushButton_plot')
        # QRadioButton
        self.radioButton_real_part = self.findChild(QRadioButton, 'radioButton_real_part')
        self.radioButton_absolute = self.findChild(QRadioButton, 'radioButton_absolute')
        # QTreeWidget
        self.treeWidget_frequencies = self.findChild(QTreeWidget, 'treeWidget_frequencies')
        self.treeWidget_frequencies.setColumnWidth(0, 120)
        self.treeWidget_frequencies.setColumnWidth(1, 140)
        self.treeWidget_frequencies.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_frequencies.headerItem().setTextAlignment(1, Qt.AlignCenter)


    def _create_connections(self):
        self.pushButton_plot.clicked.connect(self.confirm_selection)
        self.radioButton_absolute.clicked.connect(self.radioButtonEvent)
        self.radioButton_real_part.clicked.connect(self.radioButtonEvent)
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)


    def radioButtonEvent(self):
        if self.lineEdit_natural_frequency.text() != "":
            self.check_selected_frequency()


    def get_dict_modes_frequencies(self):
        modes = np.arange(1,len(self.natural_frequencies)+1,1)
        self.dict_modes_frequencies = dict(zip(modes, self.natural_frequencies))


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_selection()
        elif event.key() == Qt.Key_Escape:
            self.close()


    def check_selected_frequency(self):
        message = ""
        if self.lineEdit_natural_frequency.text() == "":
            title = "Additional action required to plot the results"
            message = "You should select a natural frequency from the available\n\n"
            message += "list before trying to plot the acoustic mode shape."
            self.text_data = [title, message, window_title_2]
        else:
            self.project.analysis_type_label = "Acoustic Modal Analysis"
            frequency = self.selected_natural_frequency
            self.mode_index = self.natural_frequencies.index(frequency)
            absolute = self.radioButton_absolute.isChecked()
            self.opv.plot_pressure_field(self.mode_index, absolute=absolute)

        if message != "":
            PrintMessageInput(self.text_data)
            return True
        else:
            return False


    def confirm_selection(self):
        if self.check_selected_frequency():
            return
        self.complete = True
        # self.close()


    def load_natural_frequencies(self):
        self.get_dict_modes_frequencies()

        for mode, natural_frequency in self.dict_modes_frequencies.items():
            new = QTreeWidgetItem([str(mode), str(round(natural_frequency,4))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)


    def on_click_item(self, item):
        self.selected_natural_frequency = self.dict_modes_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(round(self.selected_natural_frequency,4)))


    def on_doubleclick_item(self, item):
        natural_frequency = self.dict_modes_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(natural_frequency))
        self.confirm_selection()