#fmt: off

from PyQt5.QtWidgets import QComboBox, QDialog, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

import os
import numpy as np
from pathlib import Path

window_title = "Error"

class PrescribedDofsInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ui_path = UI_DIR / "model/setup/structural/prescribed_dofs_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.project = app().project
        self.properties = app().project.model.properties
        self.preprocessor = app().project.preprocessor

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        self._config_widgets()
        self.selection_callback()
        self.load_nodes_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.keep_window_open = True
        self.list_frequencies = list()

        self.list_Nones = [None, None, None, None, None, None]
        self.dofs_labels = np.array(['Ux','Uy','Uz','Rx','Ry','Rz'])

        self.reset_table_variables()
        self.before_run = self.project.get_pre_solution_model_checks()

    def reset_table_variables(self):

        self.ux_table_values = None
        self.uy_table_values = None
        self.uz_table_values = None
        self.rx_table_values = None
        self.ry_table_values = None
        self.rz_table_values = None

        self.ux_array = None
        self.uy_array = None
        self.uz_array = None
        self.rx_array = None
        self.ry_array = None
        self.rz_array = None

        self.ux_table_path = None
        self.uy_table_path = None
        self.uz_table_path = None
        self.rx_table_path = None
        self.ry_table_path = None
        self.rz_table_path = None

        self.ux_table_name = None
        self.uy_table_name = None
        self.uz_table_name = None
        self.rx_table_name = None
        self.ry_table_name = None
        self.rz_table_name = None

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_linear_data_type : QComboBox
        self.comboBox_angular_data_type : QComboBox

        # QLineEdit
        self.lineEdit_selection_id : QLineEdit
        self.lineEdit_real_ux : QLineEdit
        self.lineEdit_real_uy : QLineEdit
        self.lineEdit_real_uz : QLineEdit
        self.lineEdit_real_rx : QLineEdit
        self.lineEdit_real_ry : QLineEdit
        self.lineEdit_real_rz : QLineEdit
        self.lineEdit_real_alldofs : QLineEdit
        #
        self.lineEdit_imag_ux : QLineEdit
        self.lineEdit_imag_uy : QLineEdit
        self.lineEdit_imag_uz : QLineEdit
        self.lineEdit_imag_rx : QLineEdit
        self.lineEdit_imag_ry : QLineEdit
        self.lineEdit_imag_rz : QLineEdit
        #
        self.lineEdit_imag_alldofs : QLineEdit
        self.lineEdit_path_table_ux : QLineEdit
        self.lineEdit_path_table_uy : QLineEdit
        self.lineEdit_path_table_uz : QLineEdit
        self.lineEdit_path_table_rx : QLineEdit
        self.lineEdit_path_table_ry : QLineEdit
        self.lineEdit_path_table_rz : QLineEdit
        self._create_list_lineEdits()

        # QPushButton
        self.pushButton_load_ux_table : QPushButton
        self.pushButton_load_uy_table : QPushButton
        self.pushButton_load_uz_table : QPushButton
        self.pushButton_load_rx_table : QPushButton
        self.pushButton_load_ry_table : QPushButton
        self.pushButton_load_rz_table : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton
        self.pushButton_constant_value_confirm : QPushButton
        self.pushButton_table_values_confirm : QPushButton

        # QTabWidget
        self.tabWidget_prescribed_dofs : QTabWidget

        # QTreeWidget
        self.treeWidget_prescribed_dofs : QTreeWidget

    def _create_list_lineEdits(self):
        self.list_lineEdit_constant_values = [  [self.lineEdit_real_ux, self.lineEdit_imag_ux],
                                                [self.lineEdit_real_uy, self.lineEdit_imag_uy],
                                                [self.lineEdit_real_uz, self.lineEdit_imag_uz],
                                                [self.lineEdit_real_rx, self.lineEdit_imag_rx],
                                                [self.lineEdit_real_ry, self.lineEdit_imag_ry],
                                                [self.lineEdit_real_rz, self.lineEdit_imag_rz]  ]

        self.list_lineEdit_table_values = [ self.lineEdit_path_table_ux,
                                            self.lineEdit_path_table_uy,
                                            self.lineEdit_path_table_uz,
                                            self.lineEdit_path_table_rx,
                                            self.lineEdit_path_table_ry,
                                            self.lineEdit_path_table_rz ]

    def _config_widgets(self):
        self.treeWidget_prescribed_dofs.setColumnWidth(0, 80)
        # self.treeWidget_prescribed_dofs.setColumnWidth(1, 60)
        #
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

    def _create_connections(self):
        #
        self.pushButton_constant_value_confirm.clicked.connect(self.constant_values_attribution_callback)
        self.pushButton_table_values_confirm.clicked.connect(self.table_values_attribution_callback)
        self.pushButton_remove.clicked.connect(self.remove_bc_from_node)
        self.pushButton_load_ux_table.clicked.connect(self.load_ux_table)
        self.pushButton_load_uy_table.clicked.connect(self.load_uy_table)
        self.pushButton_load_uz_table.clicked.connect(self.load_uz_table)
        self.pushButton_load_rx_table.clicked.connect(self.load_rx_table)
        self.pushButton_load_ry_table.clicked.connect(self.load_ry_table)
        self.pushButton_load_rz_table.clicked.connect(self.load_rz_table)
        self.pushButton_reset.clicked.connect(self.reset_all)
        #
        self.tabWidget_prescribed_dofs.currentChanged.connect(self.tabWidget_selection_event)
        #
        self.treeWidget_prescribed_dofs.itemClicked.connect(self.on_click_item)
        self.treeWidget_prescribed_dofs.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        self.reset_input_fields()
        selected_nodes = app().main_window.list_selected_nodes()

        if selected_nodes:

            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_selection_id.setText(text)

            for (property, node_id), data in self.properties.nodal_properties.items():
                if property == "prescribed_dofs" and selected_nodes[0] == node_id:

                    values = data["values"]
    
                    if "table paths" in data.keys():
                        table_paths = data["table paths"]
                        self.tabWidget_prescribed_dofs.setCurrentIndex(1)
                        for index, lineEdit_table in enumerate(self.list_lineEdit_table_values):
                            table_path = table_paths[index]
                            if table_path is not None:                   
                                lineEdit_table.setText(table_path)

                    else:
                        for index, [lineEdit_real, lineEdit_imag] in enumerate(self.list_lineEdit_constant_values):
                            if values[index] is not None:
                                lineEdit_real.setText(str(np.real(values[index])))
                                lineEdit_imag.setText(str(np.imag(values[index])))

    def check_complex_entries(self, lineEdit_real, lineEdit_imag, label):

        stop = False
        if lineEdit_real.text() != "":
            try:
                _real = float(lineEdit_real.text())
            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for real part of {label}."
                PrintMessageInput([window_title, title, message])
                lineEdit_real.setFocus()
                stop = True
                return stop, None
        else:
            _real = None

        if lineEdit_imag.text() != "":
            try:
                _imag = float(lineEdit_imag.text())
            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for imaginary part of {label}."
                PrintMessageInput([window_title, title, message])
                lineEdit_imag.setFocus()
                stop = True
                return stop, None
        else:
            _imag = None
        
        if label == 'all dofs':

            if _real is None and _imag is None:
                value = None
            elif _real is None:
                value = 1j*_imag
            elif _imag is None:
                value = complex(_real)
            else:
                value = _real + 1j*_imag
            output = [value, value, value, value, value, value] 

        else:

            if _real is None and _imag is None:
                output = None
            elif _real is None:
                output = 1j*_imag
            elif _imag is None:
                output = complex(_real)
            else:             
                output = _real + 1j*_imag

        return stop, output

    def constant_values_attribution_callback(self):

        str_nodes = self.lineEdit_selection_id.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_selection_id.setFocus()
            return

        if self.lineEdit_real_alldofs.text() != "" or self.lineEdit_imag_alldofs.text() != "":
            stop, prescribed_dofs = self.check_complex_entries(self.lineEdit_real_alldofs, self.lineEdit_imag_alldofs, "all dofs")
            if stop:
                return 
        else:    

            stop, ux = self.check_complex_entries(self.lineEdit_real_ux, self.lineEdit_imag_ux, "Ux")
            if stop:
                return
            stop, uy = self.check_complex_entries(self.lineEdit_real_uy, self.lineEdit_imag_uy, "Uy")
            if stop:
                return        
            stop, uz = self.check_complex_entries(self.lineEdit_real_uz, self.lineEdit_imag_uz, "Uz")
            if stop:
                return        
                
            stop, rx = self.check_complex_entries(self.lineEdit_real_rx, self.lineEdit_imag_rx, "Rx")
            if stop:
                return        
            stop, ry = self.check_complex_entries(self.lineEdit_real_ry, self.lineEdit_imag_ry, "Ry")
            if stop:
                return        
            stop, rz = self.check_complex_entries(self.lineEdit_real_rz, self.lineEdit_imag_rz, "Rz")
            if stop:
                return

            prescribed_dofs = [ux, uy, uz, rx, ry, rz]

        if prescribed_dofs.count(None) != 6:

            table_names = self.list_Nones
            data = [prescribed_dofs, table_names]

            self.remove_table_files_from_nodes(node_ids)
            self.remove_conflictant_excitations(node_ids)

            # self.preprocessor.set_prescribed_dofs(node_ids, data)

            real_values = [value if value is None else np.real(value) for value in prescribed_dofs]
            imag_values = [value if value is None else np.imag(value) for value in prescribed_dofs]

            for node_id in node_ids:

                coords = np.round(self.preprocessor.nodes[node_id].coordinates, 5)

                bc_data = {
                            "coords" : list(coords),
                            "values" : prescribed_dofs,
                            "real values" : real_values,
                            "imag values" : imag_values
                          }

                self.properties._set_property("prescribed_dofs", bc_data, node_ids=node_id)

            app().pulse_file.write_model_properties_in_file()
            app().main_window.update_plots()
            self.close()

            print(f"[Set Prescribed DOF] - defined at node(s) {node_ids}")  

        else:
            title = "Additional inputs required"
            message = "You must inform at least one prescribed dof\n"
            message += "before confirming the input!"
            PrintMessageInput([window_title, title, message]) 

    def load_table(self, lineEdit : QLineEdit, dof_label : str, direct_load = False):

        title = "Error while loading table"

        try:
            if direct_load:
                path_imported_table = lineEdit.text()

            else:

                last_path = app().main_window.config.get_last_folder_for("imported table folder")
                if last_path is None:
                    last_path = str(Path().home())

                caption = f"Choose a table to import the {dof_label} nodal load"
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
        
            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum "
                message += "data must have frequencies, real and imaginary columns."
                PrintMessageInput([window_title, title, message])
                lineEdit.setFocus()
                return None, None

            imported_values = imported_file[:,1] + 1j*imported_file[:,2]

            self.frequencies = imported_file[:,0]
            self.f_min = self.frequencies[0]
            self.f_max = self.frequencies[-1]
            self.f_step = self.frequencies[1] - self.frequencies[0]

            app().main_window.config.write_last_folder_path_in_file("imported table folder", path_imported_table)

            if self.project.change_project_frequency_setup(imported_filename, list(self.frequencies)):
                return None, None
            else:
                self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)
            
            return imported_values, path_imported_table

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title, title, message])
            lineEdit.setFocus()
            return None, None

    def load_ux_table(self):
        self.ux_table_values, self.ux_table_path = self.load_table(self.lineEdit_path_table_ux, "Ux")
        if  self.ux_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_ux)

    def load_uy_table(self):
        self.uy_table_values, self.uy_table_path = self.load_table(self.lineEdit_path_table_uy, "Uy")
        if self.uy_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_uy)
            
    def load_uz_table(self):
        self.uz_table_values, self.uz_table_path = self.load_table(self.lineEdit_path_table_uz, "Uz")
        if self.uz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_uz)
            
    def load_rx_table(self):
        self.rx_table_values, self.rx_table_path = self.load_table(self.lineEdit_path_table_rx, "Rx")
        if self.rx_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_rx)
            
    def load_ry_table(self):
        self.ry_table_values, self.ry_table_path = self.load_table(self.lineEdit_path_table_ry, "Ry")
        if self.ry_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_ry)
            
    def load_rz_table(self):
        self.rz_table_values, self.rz_table_path = self.load_table(self.lineEdit_path_table_rz, "Rz")
        if self.rz_table_path is None:
            self.lineEdit_reset(self.lineEdit_path_table_rz)

    def lineEdit_reset(self, lineEdit : QLineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def integrate_and_save_table_files(self, dof_label: str, node_id: int, values: np.ndarray, linear=False, angular=False):

        if self.frequencies[0]==0:
            self.frequencies[0] = float(1e-6)

        if linear:

            index_lin = self.comboBox_linear_data_type.currentIndex() 
            if index_lin == 0:
                values = values

            elif index_lin == 1:
                values = values/(1j*2*np.pi*self.frequencies)

            elif index_lin == 2:
                values = values/((1j*2*np.pi*self.frequencies)**2)

        if angular:

            index_ang = self.comboBox_angular_data_type.currentIndex()
            if index_ang == 0:
                values = values

            elif index_ang == 1:
                values = values/(1j*2*np.pi*self.frequencies)

            elif index_ang == 2:              
                values = values/((1j*2*np.pi*self.frequencies)**2)

        if self.frequencies[0] == float(1e-6):
            self.frequencies[0] = 0

        table_name = f"prescribed_dof_{dof_label}_node_{node_id}"

        real_values = np.real(values)
        imag_values = np.imag(values)
        data = np.array([self.frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("structural", table_name, data)

        return table_name, data

    def table_values_attribution_callback(self):

        str_nodes = self.lineEdit_selection_id.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_selection_id.setFocus()
            return

        table_names = self.properties.get_nodal_related_table_names("prescribed_dofs", node_ids)

        if self.ux_table_path is None:
            self.ux_table_values, self.ux_table_path = self.load_table(self.lineEdit_path_table_ux, "Ux", direct_load = True)

        if self.uy_table_path is None:
            self.uy_table_values, self.uy_table_path = self.load_table(self.lineEdit_path_table_uy, "Uy", direct_load = True)

        if self.uz_table_path is None:
            self.uz_table_values, self.uz_table_path = self.load_table(self.lineEdit_path_table_uz, "Uz", direct_load = True)

        if self.rx_table_path is None:
            self.rx_table_values, self.rx_table_path = self.load_table(self.lineEdit_path_table_rx, "Rx", direct_load = True)

        if self.ry_table_path is None:
            self.ry_table_values, self.ry_table_path = self.load_table(self.lineEdit_path_table_ry, "Ry", direct_load = True)

        if self.rz_table_path is None:
            self.rz_table_values, self.rz_table_path = self.load_table(self.lineEdit_path_table_rz, "Rz", direct_load = True)

        for node_id in node_ids:
            
            if self.ux_table_values is not None:
                self.ux_table_name, self.ux_array = self.integrate_and_save_table_files("Ux", node_id, self.ux_table_values, self.ux_table_path, linear = True)

            if self.uy_table_values is not None:
                self.uy_table_name, self.uy_array = self.integrate_and_save_table_files("Uy", node_id, self.uy_table_values, self.uy_table_path, linear = True)

            if self.uz_table_values is not None:
                self.uz_table_name, self.uz_array = self.integrate_and_save_table_files("Uz", node_id, self.uz_table_values, self.uz_table_path, linear = True)

            if self.rx_table_values is not None:
                self.rx_table_name, self.rx_array = self.integrate_and_save_table_files("Rx", node_id, self.rx_table_values, self.rx_table_path, linear = True)

            if self.ry_table_values is not None:
                self.ry_table_name, self.rx_array = self.integrate_and_save_table_files("Ry", node_id, self.ry_table_values, self.ry_table_path, linear = True)

            if self.rz_table_values is not None:
                self.rz_table_name, self.rx_array = self.integrate_and_save_table_files("Rz", node_id, self.rz_table_values, self.rz_table_path, linear = True)

            basenames = [   self.ux_table_name, self.uy_table_name, self.uz_table_name, 
                            self.rx_table_name, self.ry_table_name, self.rz_table_name   ]

            table_paths = [ self.ux_table_path, self.uy_table_path, self.uz_table_path, 
                            self.rx_table_path, self.ry_table_path, self.rz_table_path ]

            prescribed_dofs = [ self.ux_table_values, self.uy_table_values, self.uz_table_values, 
                                self.rx_table_values, self.ry_table_values, self.rz_table_values ]
            
            array_data = [  self.ux_array, self.uy_array, self.uz_array, 
                            self.rx_array, self.ry_array, self.rz_array  ]

            data = [prescribed_dofs, basenames]

            if basenames == self.list_Nones:
                title = "Additional inputs required"
                message = "You must inform at least one prescribed dof "
                message += "table path before confirming the input!"
                PrintMessageInput([window_title, title, message]) 
                return 
                
            coords = np.round(self.preprocessor.nodes[node_id].coordinates, 5)

            bc_data = {
                        "coords" : list(coords),
                        "table names" : basenames,
                        "table paths" : table_paths,
                        "values" : prescribed_dofs,
                        "data arrays" : array_data
                       }

            self.properties._set_property("prescribed_dofs", bc_data, node_ids=node_id)

        # self.preprocessor.set_prescribed_dofs(node_ids, data)

        app().pulse_file.write_model_properties_in_file()
        app().pulse_file.write_imported_table_data_in_file()

        self.process_table_file_removal(table_names)

        app().main_window.update_plots()
        self.close()

        print(f"[Set Prescribed DOF] - defined at node(s) {node_ids}")

    def text_label(self, mask):

        text = ""
        labels = self.dofs_labels[mask]

        if list(mask).count(True) == 6:
            text = "[{}, {}, {}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 5:
            text = "[{}, {}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 4:
            text = "[{}, {}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 3:
            text = "[{}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 2:
            text = "[{}, {}]".format(*labels)
        elif list(mask).count(True) == 1:
            text = "[{}]".format(*labels)

        return text

    def load_nodes_info(self):

        self.treeWidget_prescribed_dofs.clear()
        for (property, node_id), data in self.properties.nodal_properties.items():

            if property == "prescribed_dofs":
                values = data["values"]
                constrained_dofs_mask = [False if value is None else True for value in values]
                new = QTreeWidgetItem([str(node_id), str(self.text_label(constrained_dofs_mask))])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_prescribed_dofs.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        self.tabWidget_prescribed_dofs.setTabVisible(2, False)
        for (property, _) in self.properties.nodal_properties.keys():
            if property == "prescribed_dofs":
                self.tabWidget_prescribed_dofs.setCurrentIndex(0)
                self.tabWidget_prescribed_dofs.setTabVisible(2, True)
                return

    def tabWidget_selection_event(self):
        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_prescribed_dofs.currentIndex() == 2:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)
            self.selection_callback()

    def on_click_item(self, item):
        self.pushButton_remove.setDisabled(False)
        self.lineEdit_selection_id.setText(item.text(0))

    def on_double_click_item(self, item):
        # self.on_click_item(item)
        self.lineEdit_selection_id.setText(item.text(0))
        self.get_nodal_info(item)

    def get_nodal_info(self, item):
        try:

            loads_info = dict()
            selected_node = int(item.text(0))

            for (property, node_id), data in self.properties.nodal_properties.items():
                if property == "prescribed_dofs" and selected_node == node_id:

                    values = data["values"]
                    nodal_loads_mask = [False if bc is None else True for bc in values]

                    for i, _bool in enumerate(nodal_loads_mask):
                        if _bool:
                            dof_label = self.dofs_labels[i]
                            loads_info[selected_node, dof_label] = values[i]

            if len(loads_info):

                self.hide()
                header_labels = ["Node ID", "DOF label", "Value"]
                GetInformationOfGroup(  group_label = "Prescribed dofs",
                                        selection_label = "Node ID:",
                                        header_labels = header_labels,
                                        column_widths = [70, 140, 150],
                                        data = data  )

        except Exception as error_log:
            title = "Error while gathering prescribed dofs information"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])
            return

    def remove_conflictant_excitations(self, node_ids: int | list | tuple):

        if isinstance(node_ids, int):
            node_ids = [node_ids]

        for node_id in node_ids:
            for label in ["nodal_loads"]:
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
                self.properties._remove_nodal_property("prescribed_dofs", node_id)

            app().pulse_file.write_model_properties_in_file()

            data = [self.list_Nones, self.list_Nones]
            # self.preprocessor.set_prescribed_dofs(node_ids, data)

            self.lineEdit_selection_id.setText("")
            self.pushButton_remove.setDisabled(True)
            self.load_nodes_info()

            app().main_window.update_plots()
            # self.close()

    def remove_table_files_from_nodes(self, node_ids : list):
        table_names = self.properties.get_nodal_related_table_names("prescribed_dofs", node_ids, equals=True)
        self.process_table_file_removal(table_names)

    def reset_all(self):

        self.hide()

        title = "Resetting of prescribed dofs"
        message = "Would you like to remove all prescribed dofs from the structural model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            
            node_ids = list()
            for (property, node_id), data in self.properties.nodal_properties.items():
                if property == "prescribed_dofs":
                    node_ids.append(node_id)

            self.remove_table_files_from_nodes(node_ids)

            data = [self.list_Nones, self.list_Nones]
            # self.preprocessor.set_prescribed_dofs(node_ids, data)

            self.properties._reset_property("prescribed_dofs")
            app().pulse_file.write_model_properties_in_file()
            app().main_window.update_plots()
            self.close()

    def process_table_file_removal(self, table_names : list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("structural", table_name)
            app().pulse_file.write_imported_table_data_in_file()

    def reset_input_fields(self):
        self.lineEdit_selection_id.setText("")
        for [lineEdit_real, lineEdit_imag] in self.list_lineEdit_constant_values:
            lineEdit_real.setText("")
            lineEdit_imag.setText("")
        for lineEdit_table in self.list_lineEdit_table_values:
            lineEdit_table.setText("")
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_prescribed_dofs.currentIndex()==0:
                self.constant_values_attribution_callback()
            elif self.tabWidget_prescribed_dofs.currentIndex()==1:
                self.table_values_attribution_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)

#fmt: on