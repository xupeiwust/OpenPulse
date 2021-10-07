# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Kula\Petrobras\temp3\OpenPulse\data\user_input\ui\Project\getStarted.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(650, 424)
        Form.setMinimumSize(QtCore.QSize(650, 424))
        Form.setMaximumSize(QtCore.QSize(650, 424))
        Form.setSizeIncrement(QtCore.QSize(0, 0))
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(434, 120, 211, 293))
        self.widget.setObjectName("widget")
        self.load_button = QtWidgets.QPushButton(self.widget)
        self.load_button.setGeometry(QtCore.QRect(0, 60, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.load_button.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("c:\\Users\\Kula\\Petrobras\\temp3\\OpenPulse\\data\\user_input\\ui\\Project\\../../../data/icons/loadProject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.load_button.setIcon(icon)
        self.load_button.setIconSize(QtCore.QSize(40, 45))
        self.load_button.setDefault(False)
        self.load_button.setObjectName("load_button")
        self.create_button = QtWidgets.QPushButton(self.widget)
        self.create_button.setGeometry(QtCore.QRect(0, 0, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.create_button.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("c:\\Users\\Kula\\Petrobras\\temp3\\OpenPulse\\data\\user_input\\ui\\Project\\../../../data/icons/012-favorite.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.create_button.setIcon(icon1)
        self.create_button.setIconSize(QtCore.QSize(40, 45))
        self.create_button.setDefault(False)
        self.create_button.setObjectName("create_button")
        self.reset_list_projects_button = QtWidgets.QPushButton(self.widget)
        self.reset_list_projects_button.setGeometry(QtCore.QRect(0, 120, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.reset_list_projects_button.setFont(font)
        self.reset_list_projects_button.setStyleSheet("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("c:\\Users\\Kula\\Petrobras\\temp3\\OpenPulse\\data\\user_input\\ui\\Project\\../../../data/icons/pulse.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reset_list_projects_button.setIcon(icon2)
        self.reset_list_projects_button.setIconSize(QtCore.QSize(40, 45))
        self.reset_list_projects_button.setObjectName("reset_list_projects_button")
        self.continue_button = QtWidgets.QPushButton(self.widget)
        self.continue_button.setGeometry(QtCore.QRect(0, 242, 203, 23))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.continue_button.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.continue_button.setFont(font)
        self.continue_button.setFlat(True)
        self.continue_button.setObjectName("continue_button")
        self.checkBox = QtWidgets.QCheckBox(self.widget)
        self.checkBox.setGeometry(QtCore.QRect(8, 272, 199, 17))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.about_button = QtWidgets.QPushButton(self.widget)
        self.about_button.setGeometry(QtCore.QRect(0, 180, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.about_button.setFont(font)
        self.about_button.setStyleSheet("")
        self.about_button.setIcon(icon2)
        self.about_button.setIconSize(QtCore.QSize(40, 45))
        self.about_button.setObjectName("about_button")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(0, 70, 650, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(36, 4, 579, 40))
        font = QtGui.QFont()
        font.setFamily("Linux Biolinum G")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(36, 48, 579, 25))
        self.label_2.setMinimumSize(QtCore.QSize(0, 25))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.recents_label = QtWidgets.QLabel(Form)
        self.recents_label.setGeometry(QtCore.QRect(28, 90, 377, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.recents_label.setFont(font)
        self.recents_label.setAutoFillBackground(True)
        self.recents_label.setAlignment(QtCore.Qt.AlignCenter)
        self.recents_label.setObjectName("recents_label")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(436, 90, 189, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAutoFillBackground(True)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.widget_project1 = QtWidgets.QWidget(Form)
        self.widget_project1.setGeometry(QtCore.QRect(22, 116, 387, 61))
        self.widget_project1.setObjectName("widget_project1")
        self.project1_button = QtWidgets.QPushButton(self.widget_project1)
        self.project1_button.setGeometry(QtCore.QRect(298, 4, 87, 52))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.project1_button.setFont(font)
        self.project1_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.project1_button.setAutoFillBackground(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("c:\\Users\\Kula\\Petrobras\\temp3\\OpenPulse\\data\\user_input\\ui\\Project\\../../../data/icons/002-analysis.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.project1_button.setIcon(icon3)
        self.project1_button.setAutoDefault(False)
        self.project1_button.setDefault(False)
        self.project1_button.setFlat(False)
        self.project1_button.setObjectName("project1_button")
        self.project1_path_label = QtWidgets.QLabel(self.widget_project1)
        self.project1_path_label.setGeometry(QtCore.QRect(4, 4, 290, 52))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setItalic(False)
        self.project1_path_label.setFont(font)
        self.project1_path_label.setFrameShape(QtWidgets.QFrame.Box)
        self.project1_path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.project1_path_label.setWordWrap(True)
        self.project1_path_label.setObjectName("project1_path_label")
        self.widget_project2 = QtWidgets.QWidget(Form)
        self.widget_project2.setGeometry(QtCore.QRect(22, 176, 387, 61))
        self.widget_project2.setObjectName("widget_project2")
        self.project2_button = QtWidgets.QPushButton(self.widget_project2)
        self.project2_button.setGeometry(QtCore.QRect(298, 4, 87, 52))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.project2_button.setFont(font)
        self.project2_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.project2_button.setAutoFillBackground(False)
        self.project2_button.setIcon(icon3)
        self.project2_button.setAutoDefault(True)
        self.project2_button.setDefault(False)
        self.project2_button.setFlat(False)
        self.project2_button.setObjectName("project2_button")
        self.project2_path_label = QtWidgets.QLabel(self.widget_project2)
        self.project2_path_label.setGeometry(QtCore.QRect(4, 4, 290, 52))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setItalic(False)
        self.project2_path_label.setFont(font)
        self.project2_path_label.setFrameShape(QtWidgets.QFrame.Box)
        self.project2_path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.project2_path_label.setWordWrap(True)
        self.project2_path_label.setObjectName("project2_path_label")
        self.widget_project3 = QtWidgets.QWidget(Form)
        self.widget_project3.setGeometry(QtCore.QRect(22, 236, 387, 61))
        self.widget_project3.setObjectName("widget_project3")
        self.project3_button = QtWidgets.QPushButton(self.widget_project3)
        self.project3_button.setGeometry(QtCore.QRect(298, 4, 87, 52))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.project3_button.setFont(font)
        self.project3_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.project3_button.setAutoFillBackground(False)
        self.project3_button.setIcon(icon3)
        self.project3_button.setAutoDefault(True)
        self.project3_button.setDefault(False)
        self.project3_button.setFlat(False)
        self.project3_button.setObjectName("project3_button")
        self.project3_path_label = QtWidgets.QLabel(self.widget_project3)
        self.project3_path_label.setGeometry(QtCore.QRect(4, 4, 290, 52))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setItalic(False)
        self.project3_path_label.setFont(font)
        self.project3_path_label.setFrameShape(QtWidgets.QFrame.Box)
        self.project3_path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.project3_path_label.setWordWrap(True)
        self.project3_path_label.setObjectName("project3_path_label")
        self.widget_project4 = QtWidgets.QWidget(Form)
        self.widget_project4.setGeometry(QtCore.QRect(22, 296, 387, 61))
        self.widget_project4.setObjectName("widget_project4")
        self.project4_button = QtWidgets.QPushButton(self.widget_project4)
        self.project4_button.setGeometry(QtCore.QRect(298, 4, 87, 52))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.project4_button.setFont(font)
        self.project4_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.project4_button.setAutoFillBackground(False)
        self.project4_button.setIcon(icon3)
        self.project4_button.setAutoDefault(True)
        self.project4_button.setDefault(False)
        self.project4_button.setFlat(False)
        self.project4_button.setObjectName("project4_button")
        self.project4_path_label = QtWidgets.QLabel(self.widget_project4)
        self.project4_path_label.setGeometry(QtCore.QRect(4, 4, 290, 52))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setItalic(False)
        self.project4_path_label.setFont(font)
        self.project4_path_label.setFrameShape(QtWidgets.QFrame.Box)
        self.project4_path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.project4_path_label.setWordWrap(True)
        self.project4_path_label.setObjectName("project4_path_label")
        self.widget_project5 = QtWidgets.QWidget(Form)
        self.widget_project5.setGeometry(QtCore.QRect(22, 356, 387, 61))
        self.widget_project5.setObjectName("widget_project5")
        self.project5_button = QtWidgets.QPushButton(self.widget_project5)
        self.project5_button.setGeometry(QtCore.QRect(298, 4, 87, 52))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.project5_button.setFont(font)
        self.project5_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.project5_button.setAutoFillBackground(False)
        self.project5_button.setIcon(icon3)
        self.project5_button.setAutoDefault(True)
        self.project5_button.setDefault(False)
        self.project5_button.setFlat(False)
        self.project5_button.setObjectName("project5_button")
        self.project5_path_label = QtWidgets.QLabel(self.widget_project5)
        self.project5_path_label.setGeometry(QtCore.QRect(4, 4, 290, 52))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setItalic(False)
        self.project5_path_label.setFont(font)
        self.project5_path_label.setFrameShape(QtWidgets.QFrame.Box)
        self.project5_path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.project5_path_label.setWordWrap(True)
        self.project5_path_label.setObjectName("project5_path_label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.create_button, self.load_button)
        Form.setTabOrder(self.load_button, self.reset_list_projects_button)
        Form.setTabOrder(self.reset_list_projects_button, self.about_button)
        Form.setTabOrder(self.about_button, self.project1_button)
        Form.setTabOrder(self.project1_button, self.project2_button)
        Form.setTabOrder(self.project2_button, self.project3_button)
        Form.setTabOrder(self.project3_button, self.project4_button)
        Form.setTabOrder(self.project4_button, self.project5_button)
        Form.setTabOrder(self.project5_button, self.continue_button)
        Form.setTabOrder(self.continue_button, self.checkBox)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OpenPulse - Get Started"))
        self.load_button.setText(_translate("Form", "Open a local Project"))
        self.create_button.setText(_translate("Form", "Create a new Project"))
        self.reset_list_projects_button.setText(_translate("Form", "Reset list of Projects"))
        self.continue_button.setText(_translate("Form", "Continue without a project ->"))
        self.checkBox.setText(_translate("Form", "Do not show this dialog again"))
        self.about_button.setText(_translate("Form", "About Open Pulse"))
        self.label.setText(_translate("Form", "OpenPulse"))
        self.label_2.setText(_translate("Form", "Open Source Software for Pulsation Analysis of Pipeline Systems"))
        self.recents_label.setText(_translate("Form", "Recents Projects"))
        self.label_4.setText(_translate("Form", "Get Started"))
        self.project1_button.setText(_translate("Form", "Load \n"
"project"))
        self.project1_path_label.setText(_translate("Form", "Project path 1"))
        self.project2_button.setText(_translate("Form", "Load\n"
"Project"))
        self.project2_path_label.setText(_translate("Form", "Project path 2"))
        self.project3_button.setText(_translate("Form", "Load\n"
"Project"))
        self.project3_path_label.setText(_translate("Form", "Project path 3"))
        self.project4_button.setText(_translate("Form", "Load\n"
"Project"))
        self.project4_path_label.setText(_translate("Form", "Project path 4"))
        self.project5_button.setText(_translate("Form", "Load\n"
"Project"))
        self.project5_path_label.setText(_translate("Form", "Project path 5"))