# fmt: off

from PyQt5.QtWidgets import QComboBox, QDialog, QCheckBox, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.print_message import PrintMessageInput

import numpy as np


window_title_1 = "Error"
window_title_2 = "Warning"

class DecouplingRotationDOFsInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/decoupling_rotation_dofs_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_decoupling_info()
        self.selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.keep_window_open = True
        self.complete = False

        self.before_run = app().project.get_pre_solution_model_checks() 

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_rotation_x: QCheckBox
        self.checkBox_rotation_y: QCheckBox
        self.checkBox_rotation_z: QCheckBox

        # QComboBox
        self.comboBox_node_to_uncouple_dofs: QComboBox

        # QLineEdit
        self.lineEdit_decoupled_dofs: QLineEdit
        self.lineEdit_selected_group: QLineEdit
        self.lineEdit_node_IDs: QLineEdit
        self.lineEdit_selected_element: QLineEdit
        self.lineEdit_joint_node_id: QLineEdit

        # QPushButton       
        self.pushButton_confirm: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton

        # QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_B2PX_rotation_decoupling: QTreeWidget

    def _create_connections(self):
        #
        self.pushButton_confirm.clicked.connect(self.dofs_decoupling_attribution_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_B2PX_rotation_decoupling.itemClicked.connect(self.on_click_item)
        self.treeWidget_B2PX_rotation_decoupling.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_elements = app().main_window.list_selected_elements()

        if selected_elements:
            if len(selected_elements) == 1:

                for (property, element_id), data in self.properties.element_properties.items():
                    if property == "B2PX_decoupling_rotation" and element_id == selected_elements[0]:
                        decoupled_dofs = data["B2PX_decoupling_rotation"]
                        self.checkBox_rotation_x.setChecked(decoupled_dofs[0])
                        self.checkBox_rotation_y.setChecked(decoupled_dofs[1])
                        self.checkBox_rotation_z.setChecked(decoupled_dofs[2])
                        self.lineEdit_selected_element.setText(str(element_id))
                        return

                element_id = selected_elements[0]
                self.lineEdit_selected_element.setText(str(element_id))
                element = app().project.model.preprocessor.structural_elements[element_id]

                if element.element_type == "beam_1":
                    first_node = element.first_node.external_index
                    last_node  = element.last_node.external_index
                    if len(app().project.model.preprocessor.neighboor_elements_of_node(first_node)) == 3:
                        self.lineEdit_tjoint_node_id.setText(first_node)

                    elif len(app().project.model.preprocessor.neighboor_elements_of_node(last_node)) == 3:
                        self.lineEdit_tjoint_node_id.setText(last_node)

    def _config_widgets(self):
        for i, width in enumerate([60, 120, 140]):
            self.treeWidget_B2PX_rotation_decoupling.setColumnWidth(i, width)
            self.treeWidget_B2PX_rotation_decoupling.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def tab_event_callback(self):
        self.lineEdit_selected_group.setText("")
        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 1:
            self.pushButton_remove.setDisabled(True)  

    def on_click_item(self, item):
        self.lineEdit_selected_group.setText(item.text(0))
        self.pushButton_remove.setDisabled(False)

    def on_double_click_item(self, item):
        self.on_click_item(item)
        self.get_information(item)

    def remove_callback(self):

        if self.lineEdit_selected_group.text() != "":

            group_id = int(self.lineEdit_selected_group.text())
            [element_id, data] = self.decoupling_data[group_id]

            self.properties._remove_element_property("B2PX_rotation_decoupling", element_id)

            app().pulse_file.write_model_properties_in_file()
            self.load_decoupling_info()

    def reset_callback(self):

        self.hide()

        title = "Resetting of B2PX decoupling rotations"
        message = "Would you like to remove all B2PX decoupling rotations from the structural model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            self.properties._reset_element_property("B2PX_decoupling_rotation")
            app().pulse_file.write_model_properties_in_file()
            self.close()

    def get_rotation_mask(self):

        rotations_mask = [  self.checkBox_rotation_x.isChecked(), 
                            self.checkBox_rotation_y.isChecked(), 
                            self.checkBox_rotation_z.isChecked()  ]

        if np.sum(rotations_mask) == 0:
            title = "Invalid decoupling setup"
            message = "There are no rotation DOFs decoupling in the current setup. "
            message += "You should tick at least one rotation DOF before continue."
            PrintMessageInput([window_title_1, title, message])
            return None

        else:
            return rotations_mask

    def dofs_decoupling_attribution_callback(self):

        lineEdit = self.lineEdit_selected_element.text()
        stop, element_id = self.before_run.check_selected_ids(lineEdit, "elements", single_id = True)
        if stop:
            return

        element = app().project.model.preprocessor.structural_elements[element_id]

        if self.comboBox_node_to_uncouple_dofs.currentIndex() == 0:
            selected_node_id = element.first_node.external_index
        else:
            selected_node_id  = element.last_node.external_index

        neighboor_elements = app().project.model.preprocessor.neighboor_elements_of_node(selected_node_id)
        if len(neighboor_elements) < 3:
            title = "Incorrect Node ID selection"
            message = "The decoupling of rotation dofs can only be applied to the T connections." 
            PrintMessageInput([window_title_1, title, message])
            return
        
        element_type = element.element_type
        rotations_mask = self.get_rotation_mask()

        if len(rotations_mask):
            if element_type == 'beam_1':

                app().project.model.preprocessor.set_B2PX_rotation_decoupling(  element_id, 
                                                                                selected_node_id, 
                                                                                rotations_mask  )

                print("[Set Rotation Decoupling] - defined at element {} and at node {}".format(self.element_id, self.selected_node_id))
                self.complete = True
                self.close()

            else:

                title = "Invalid decoupling setup"
                message = f"The selected element have a '{element_type}' formulation, you should "
                message += "have a 'beam_1' element type in selection to decouple the rotation dofs. "
                message += " Try to choose another element or change the element type formulation."
                PrintMessageInput([window_title_1, title, message])
                return

    def text_label(self, mask):
        text = ""
        load_labels = np.array(['Rx','Ry','Rz'])
        labels = load_labels[mask]
        if list(mask).count(True) == 3:
            text = "[{}, {}, {}]".format(*labels)
        elif list(mask).count(True) == 2:
            text = "[{}, {}]".format(*labels)
        elif list(mask).count(True) == 1:
            text = "[{}]".format(*labels)
        return text

    def load_decoupling_info(self):

        group_id = 0
        self.decoupling_data = dict()
        self.treeWidget_B2PX_rotation_decoupling.clear()

        for (property, element_id), data in self.properties.element_properties.items():
            if property == "B2PX_decoupling_rotation":

                group_id += 1
                self.decoupling_data[group_id] = [element_id, data]

                connecting_node = data["connecting node"]
                decoupled_dofs = data["decoupled dofs"]
                decoupled_dofs_labels = self.text_label(decoupled_dofs)

                item = QTreeWidgetItem([ str(group_id), 
                                        decoupled_dofs_labels, 
                                        str(element_id), 
                                        str(connecting_node) ])

                item.setTextAlignment(0, Qt.AlignCenter)
                item.setTextAlignment(1, Qt.AlignCenter)
                item.setTextAlignment(2, Qt.AlignCenter)
                self.treeWidget_B2PX_rotation_decoupling.addTopLevelItem(item)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        self.lineEdit_selected_group.setText("")
        self.tabWidget_main.setTabVisible(1, False)
        for (property, _) in self.properties.element_properties.keys():
            if property == "B2PX_rotation_decoupling":
                self.tabWidget_main.setTabVisible(1, True)
                return

    def get_information(self, item):
        try:
            if self.lineEdit_decoupled_dofs.text() != "":

                group_id = int(item.text(0))
                [element_id, data] = self.decoupling_data[group_id]

                connecting_node = data["connecting node"]
                decoupled_dofs = data["decoupled dofs"]
                decoupled_dofs_labels = self.text_label(decoupled_dofs)  

                aux = dict()
                aux[(element_id, connecting_node)] = decoupled_dofs_labels
                
                if aux:
                    self.close()
                    header_labels = ["Element ID", "Node ID", "Decoupled DOFs"]
                    GetInformationOfGroup(  group_label = "Decoupling rotation DOFs",
                                            selection_label = "Element ID:",
                                            header_labels = header_labels,
                                            column_widths = [100, 100, 150],
                                            data = data  )

                # if read.lines_removed:
                #     self.load_decoupling_info()
                #     self.clear_texts()

            else:
                title = "Invalid selection"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([window_title_2, title, message])
                
        except Exception as error_log:
            title = "Error while getting information of selected group"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.dofs_decoupling_attribution_callback()
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)
    
# fmt: on