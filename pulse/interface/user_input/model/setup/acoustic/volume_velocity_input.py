from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QSpinBox, QTabWidget, QToolButton, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

import os
import numpy as np
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"

class VolumeVelocityInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/volume_velocity_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()

        self.selection_callback()
        self.load_nodes_info()
        
        while self.keep_window_open:
            self.exec()

    def _initialize(self):

        self.array = None
        self.table_name = None
        self.table_path = None
        self.table_values = None                

        self.keep_window_open = True

        self.before_run = app().project.get_pre_solution_model_checks()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QLineEdit
        self.lineEdit_imag_value : QLineEdit
        self.lineEdit_real_value : QLineEdit
        self.lineEdit_selection_id : QLineEdit
        self.lineEdit_table_path : QLineEdit

        # QPushButton
        self.pushButton_constant_values : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton
        self.pushButton_search : QPushButton
        self.pushButton_table_values : QPushButton

        # QSpinBox
        self.spinBox_skip_wors : QSpinBox

        # QTabWidget
        self.tabWidget_volume_velocity : QTabWidget

        # QTreeWidget
        self.treeWidget_volume_velocity : QTreeWidget
        self.treeWidget_volume_velocity.setColumnWidth(1, 20)
        self.treeWidget_volume_velocity.setColumnWidth(2, 80)

    def _create_connections(self):
        #
        self.pushButton_constant_values.clicked.connect(self.constant_values_attribution_callback)
        self.pushButton_remove.clicked.connect(self.remove_bc_from_node)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_table_values.clicked.connect(self.table_values_attribution_callback)
        self.pushButton_search.clicked.connect(self.load_volume_velocity_table)
        #
        self.tabWidget_volume_velocity.currentChanged.connect(self.tabEvent_volume_velocity)
        #
        self.treeWidget_volume_velocity.itemClicked.connect(self.on_click_item)
        self.treeWidget_volume_velocity.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        self.reset_input_fields()
        selected_nodes = app().main_window.list_selected_nodes()

        if len(selected_nodes) == 1:

            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_selection_id.setText(text)

            for (property, node_id), data in self.properties.nodal_properties.items():
                if property == "volume_velocity" and selected_nodes[0] == node_id:

                    values = data["values"]
    
                    if "table paths" in data.keys():
                        table_paths = data["table paths"]
                        self.tabWidget_volume_velocity.setCurrentIndex(1)
                        self.lineEdit_table_path.setText(table_paths[0])

                    else:
                        self.tabWidget_volume_velocity.setCurrentIndex(0)
                        self.lineEdit_real_value.setText(str(np.real(values)))
                        self.lineEdit_imag_value.setText(str(np.imag(values)))

    def tabEvent_volume_velocity(self):
        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_volume_velocity.currentIndex() == 2:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
        else:
            self.selection_callback()
            self.lineEdit_selection_id.setDisabled(False)

    def update_tabs_visibility(self):
        self.tabWidget_volume_velocity.setTabVisible(2, False)
        for (property, _) in self.properties.nodal_properties.keys():
            if property == "volume_velocity":
                self.tabWidget_volume_velocity.setCurrentIndex(0)
                self.tabWidget_volume_velocity.setTabVisible(2, True)

    def load_nodes_info(self):

        self.treeWidget_volume_velocity.clear()
        for (property, node_id), data in self.properties.nodal_properties.items():

            if property == "volume_velocity":
                values = data["values"]
                new = QTreeWidgetItem([str(node_id), str(self.text_label(values[0]))])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_volume_velocity.addTopLevelItem(new)

        self.update_tabs_visibility()

    def check_complex_entries(self, lineEdit_real: QLineEdit, lineEdit_imag: QLineEdit):

        stop = False
        title = "Invalid entry to the volume velocity"

        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                message = "Wrong input for real part of volume velocity."
                PrintMessageInput([window_title_1, title, message])
                lineEdit_real.setFocus()
                stop = True
                return stop, None
        else:
            real_F = 0

        if lineEdit_imag.text() != "":
            try:
                imag_F = float(lineEdit_imag.text())
            except Exception:
                message = "Wrong input for imaginary part of volume velocity."
                PrintMessageInput([window_title_1, title, message])
                lineEdit_imag.setFocus()
                stop = True
                return stop, None
        else:
            imag_F = 0
        
        if real_F == 0 and imag_F == 0:
            return  stop, None
        else:
            return stop, real_F + 1j*imag_F

    def constant_values_attribution_callback(self):

        lineEdit = self.lineEdit_selection_id.text()
        stop, node_ids = self.before_run.check_selected_ids(lineEdit, "nodes")
        if stop:
            self.lineEdit_selection_id.setFocus()
            return

        stop, volume_velocity = self.check_complex_entries(self.lineEdit_real_value, self.lineEdit_imag_value)

        if stop:
            return
        
        if volume_velocity is None:
            title = "Additional inputs required"
            message = "You must inform at least one volume velocity " 
            message += "before confirming the input!"
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_real_value.setFocus()

        self.remove_table_files_from_nodes(node_ids)
        self.remove_conflictant_excitations(node_ids)

        real_values = [np.real(volume_velocity)]
        imag_values = [np.imag(volume_velocity)]

        for node_id in node_ids:

            node = app().project.model.preprocessor.nodes[node_id]
            coords = list(np.round(node.coordinates, 5))

            prop_data = {   
                            "coords" : coords,
                            "real values": real_values,
                            "imag values": imag_values,
                        }

            self.properties._set_property("volume_velocity", prop_data, node_id)

        app().pulse_file.write_model_properties_in_file()
        app().main_window.update_plots()
        self.close()

        print(f"[Set Volume Velocity] - defined at node(s) {node_ids}")

    def lineEdit_reset(self, lineEdit: QLineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def save_table_file(self, node_id: int, values: np.ndarray):

        table_name = f"volume_velocity_node_{node_id}"

        real_values = np.real(values)
        imag_values = np.imag(values)
        data = np.array([self.frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return table_name, data

    def load_table(self, lineEdit: QLineEdit, direct_load=False):
        try:

            if direct_load:
                self.path_imported_table = lineEdit.text()
            else:
                last_path = app().main_window.config.get_last_folder_for("imported table folder")
                if last_path is None:
                    last_path = str(Path().home())

                caption = f"Choose a table to import the volume velocity"
                path_imported_table, check = app().main_window.file_dialog.get_open_file_name(
                                                                                                caption, 
                                                                                                last_path, 
                                                                                                'Table File (*.csv; *.dat; *.txt)'
                                                                                              )

                if not check:
                    return None, None

            if path_imported_table == "":
                return None, None

            imported_filename = os.path.basename(path_imported_table)
            lineEdit.setText(path_imported_table)         
            imported_file = np.loadtxt(path_imported_table, delimiter=",")

            title = "Error reached while loading 'volume velocity' table"
            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum"
                message += " data must have only two columns to the frequencies and values."
                PrintMessageInput([window_title_1, title, message])
                return None, None

            imported_values = imported_file[:,1]

            self.frequencies = imported_file[:,0]
            f_min = self.frequencies[0]
            f_max = self.frequencies[-1]
            f_step = self.frequencies[1] - self.frequencies[0] 

            if app().project.model.change_analysis_frequency_setup(imported_filename, list(self.frequencies)):
                self.lineEdit_reset(lineEdit)
                return None, None

            else:

                frequency_setup = { "f_min" : f_min,
                                    "f_max" : f_max,
                                    "f_step" : f_step }

                app().project.model.set_frequency_setup(frequency_setup)

            return imported_values, imported_filename

        except Exception as log_error:
            title = "Error reached while loading 'volume velocity' table"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            lineEdit.setFocus()
            return None, None

    def load_volume_velocity_table(self):
        self.table_values, self.table_path = self.load_table(self.lineEdit_table_path)

    def table_values_attribution_callback(self):

        str_nodes = self.lineEdit_selection_id.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_selection_id.setFocus()
            return

        self.remove_conflictant_excitations(node_ids)
        # table_names = self.properties.get_nodal_related_table_names("volume_velocity", node_ids)

        if self.lineEdit_table_path != "":

            if self.table_path is None:
                self.table_values, self.table_path = self.load_table(
                                                                        self.lineEdit_table_path, 
                                                                        direct_load=True
                                                                     )

                if self.table_values is None:
                    return

            for node_id in node_ids:

                self.table_name, self.array = self.save_table_file( 
                                                                    node_id, 
                                                                    self.table_values, 
                                                                    self.table_path
                                                                   )

                basenames = [self.table_name]
                table_paths = [self.table_path]
                values = [self.table_values]                
                array_data = [self.array]

                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                bc_data = {
                            "coords" : list(coords),
                            "table names" : basenames,
                            "table paths" : table_paths,
                            "values" : values,
                            "data arrays" : array_data
                        }

                self.properties._set_property("volume_velocity", bc_data, node_ids=node_id)

            app().pulse_file.write_model_properties_in_file()
            app().pulse_file.write_imported_table_data_in_file()
            # self.process_table_file_removal(table_names)
            app().main_window.update_plots()

            print(f"[Set Volume Velocity] - defined at node(s) {node_ids}")   
            self.close()

        else:
            title = "Additional inputs required"
            message = "You must inform at least one volume velocity " 
            message += "table path before confirming the input!"
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_table_path.setFocus()

    def text_label(self, value):
        text = ""
        if isinstance(value, complex):
            value_label = str(value)
        elif isinstance(value, np.ndarray):
            value_label = 'Table'
        text = "{}".format(value_label)
        return text

    def on_click_item(self, item):
        self.pushButton_remove.setDisabled(False)
        self.lineEdit_selection_id.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))
        # self.remove_bc_from_node()

    def remove_conflictant_excitations(self, node_ids: int | list | tuple):

        if isinstance(node_ids, int):
            node_ids = [node_ids]

        for node_id in node_ids:
            for label in ["acoustic_pressure", "compressor_excitation"]:
                table_names = self.properties.get_nodal_related_table_names(label, node_id)
                self.properties._remove_nodal_property(label, node_id)

                self.process_table_file_removal(table_names)

        app().pulse_file.write_model_properties_in_file()

    def remove_bc_from_node(self):

        if  self.lineEdit_selection_id.text() != "":

            str_nodes = self.lineEdit_selection_id.text()
            stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
            if stop:
                return

            self.remove_table_files_from_nodes(node_ids)

            for node_id in node_ids:
                self.properties._remove_nodal_property("volume_velocity", node_id)

            app().pulse_file.write_model_properties_in_file()

            self.lineEdit_selection_id.setText("")
            self.pushButton_remove.setDisabled(True)
            self.load_nodes_info()

            app().main_window.update_plots()
            # self.close()

    def reset_callback(self):

            self.hide()

            title = f"Resetting of volume velocities"
            message = "Would you like to remove all volume velocities from the acoustic model?"

            buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            if read._continue:

                node_ids = list()
                for (property, node_id), data in self.properties.nodal_properties.items():
                    if property == "volume_velocity":
                        node_ids.append(node_id)

                self.remove_table_files_from_nodes(node_ids)

                self.properties._reset_property("volume_velocity")
                app().pulse_file.write_model_properties_in_file()
                app().main_window.update_plots()
                self.close()

    def remove_table_files_from_nodes(self, node_ids : list):
        table_names = self.properties.get_nodal_related_table_names("volume_velocity", node_ids, equals=True)
        self.process_table_file_removal(table_names)

    def process_table_file_removal(self, table_names : list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("acoustic", table_name)
            app().pulse_file.write_imported_table_data_in_file()

    def reset_input_fields(self):
        self.lineEdit_real_value.setText("")
        self.lineEdit_imag_value.setText("")
        self.lineEdit_table_path.setText("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_volume_velocity.currentIndex()==0:
                self.check_constant_values()
            if self.tabWidget_volume_velocity.currentIndex()==1:
                self.check_table_values()
        elif event.key() == Qt.Key_Delete:
            if self.tabWidget_volume_velocity.currentIndex()==2:
                self.remove_bc_from_node()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)