from PyQt5.QtWidgets import QDialog, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import configparser

from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.aboutOpenPulseInput import AboutOpenPulseInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))

class GetStartedInput(QDialog):
    def __init__(self, project, opv, config, inputUi, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/Project/getStarted.ui'), self)

        self.icon = QIcon(get_icons_path('pulse.png'))
        self.load_icon = QIcon(get_icons_path('loadProject.png'))
        self.new_icon = QIcon(get_icons_path('add.png'))
        self.reset_icon = QIcon(get_icons_path('refresh.png'))
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.opv = opv
        self.config = config
        self.inputUi = inputUi

        self.draw = False

        self.recents_label = self.findChild(QLabel, 'recents_label')
        
        self.create_button = self.findChild(QPushButton, 'create_button')
        self.load_button = self.findChild(QPushButton, 'load_button')
        self.about_button = self.findChild(QPushButton, 'about_button')
        self.continue_button = self.findChild(QPushButton, 'continue_button')
        self.reset_list_projects_button = self.findChild(QPushButton, 'reset_list_projects_button')

        self.create_button.setIcon(self.new_icon)
        self.load_button.setIcon(self.load_icon)
        self.about_button.setIcon(self.icon)
        self.reset_list_projects_button.setIcon(self.reset_icon)

        self.create_button.clicked.connect(self.newProject)
        self.load_button.clicked.connect(self.loadProject)
        self.about_button.clicked.connect(self.aboutProject)
        self.continue_button.clicked.connect(self.continueButtonEvent)
        self.reset_list_projects_button.clicked.connect(self.reset_list_projects)

        self.project1_button = self.findChild(QPushButton, 'project1_button')
        self.project2_button = self.findChild(QPushButton, 'project2_button')
        self.project3_button = self.findChild(QPushButton, 'project3_button')
        self.project4_button = self.findChild(QPushButton, 'project4_button')
        self.project5_button = self.findChild(QPushButton, 'project5_button')
        
        self.project_buttons = []
        self.project_buttons.append(self.project1_button)
        self.project_buttons.append(self.project2_button)
        self.project_buttons.append(self.project3_button)
        self.project_buttons.append(self.project4_button)
        self.project_buttons.append(self.project5_button)
        
        self.project1_path_label = self.findChild(QLabel, 'project1_path_label')
        self.project2_path_label = self.findChild(QLabel, 'project2_path_label')
        self.project3_path_label = self.findChild(QLabel, 'project3_path_label')
        self.project4_path_label = self.findChild(QLabel, 'project4_path_label')
        self.project5_path_label = self.findChild(QLabel, 'project5_path_label')
        
        self.project_path_labels = []
        self.project_path_labels.append(self.project1_path_label)
        self.project_path_labels.append(self.project2_path_label)
        self.project_path_labels.append(self.project3_path_label)
        self.project_path_labels.append(self.project4_path_label)
        self.project_path_labels.append(self.project5_path_label)
        
        self.initial_actions()
        self.exec()

    def update_buttons_visibility(self):
        self.project_dir = []
        for i in range(5):
            self.project_dir.append("")
            self.project_buttons[i].setIcon(self.load_icon)
            self.project_buttons[i].setVisible(False)
            self.project_path_labels[i].setVisible(False)

        self.recentProjectsList = list(self.config.recentProjects.items())[::-1]
        for i in range(5 if len(self.recentProjectsList) > 5 else len(self.recentProjectsList)):
            self.project_buttons[i].setVisible(True)
            self.project_path_labels[i].setVisible(True)
            self.project_dir[i] = self.recentProjectsList[i][1]
            # text = str(self.recentProjectsList[i][0]) + "\n" + str(self.recentProjectsList[i][1])
            # self.project_buttons[i].setText(text)
            # self.project_buttons[i].setStyleSheet("text-align:right;")
            self.project_path_labels[i].setText(str(self.recentProjectsList[i][1]))
            stylesheet =    """ QLabel{ 
                                        border-radius: 6px; 
                                        border-color: rgb(150, 150, 150); 
                                        border-style: ridge; 
                                        border-width: 2px; 
                                        color: rgb(0, 0, 255); 
                                        background-color: rgb(240, 240, 240); 
                                        font: 50 9pt "MS Shell Dlg 2" 
                                        }
                            """
            self.project_path_labels[i].setStyleSheet(stylesheet)

    def initial_actions(self):
        self.update_buttons_visibility()
        self.project_buttons[0].clicked.connect(lambda: self.loadRecentProject(self.project_dir[0]))
        self.project_buttons[1].clicked.connect(lambda: self.loadRecentProject(self.project_dir[1]))
        self.project_buttons[2].clicked.connect(lambda: self.loadRecentProject(self.project_dir[2]))
        self.project_buttons[3].clicked.connect(lambda: self.loadRecentProject(self.project_dir[3]))
        self.project_buttons[4].clicked.connect(lambda: self.loadRecentProject(self.project_dir[4]))

    def continueButtonEvent(self):
        self.close()

    def newProject(self):
        if self.inputUi.new_project(self.config):
            self.draw = True
            self.close()

    def loadProject(self):
        if self.inputUi.loadProject(self.config):
            self.draw = True
            self.close()

    def aboutProject(self):
        AboutOpenPulseInput(self.project, self.opv)

    def loadRecentProject(self, dir):
        if os.path.exists(dir):
            if self.inputUi.loadProject(self.config, path=dir):
                self.draw = True
                self.close()
        else:
            read_config = configparser.ConfigParser()
            read_config.read(self.config.configFileName)
            for item, value in self.config.recentProjects.items():
                if value == dir:
                    self.config.remove_path_from_config_file(item)
                    self.update_buttons_visibility()
                    break

            title = f"Project folder not found"
            message = "The following project folder path cannot be found, "
            message += "check if the project folder have not been deleted or moved "
            message += "to another directory."
            message += f"\n\n{dir}"
            PrintMessageInput([title, message, "WARNING"])
        
    def reset_list_projects(self):
        title = f"Resetting of the recent projects list"
        message = "Dear user, do you want to proceed with the 'Recent Projects' list clean-up and resetting?\n\n"
        message += "\n\nPress the Continue button to proceed with the resetting or press Cancel or "
        message += "\nClose buttons to abort the current operation."
        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

        if read._doNotRun:
            return

        if read._continue:
            self.config.resetRecentProjectList()
            self.initial_actions()