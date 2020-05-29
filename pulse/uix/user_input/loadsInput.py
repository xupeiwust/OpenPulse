from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QPushButton
from pulse.utils import error
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

class LoadsInput(QDialog):
    def __init__(self, nodes, list_node_ids, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/loadsInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.nodes = nodes
        self.loads = None
        self.nodes_typed = []

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

        self.lineEdit_fx = self.findChild(QLineEdit, 'lineEdit_fx')
        self.lineEdit_fy = self.findChild(QLineEdit, 'lineEdit_fy')
        self.lineEdit_fz = self.findChild(QLineEdit, 'lineEdit_fz')
        self.lineEdit_mx = self.findChild(QLineEdit, 'lineEdit_mx')
        self.lineEdit_my = self.findChild(QLineEdit, 'lineEdit_my')
        self.lineEdit_mz = self.findChild(QLineEdit, 'lineEdit_mz')

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

        self.writeNodes(list_node_ids)

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_nodeID.setText(text)

    def isInteger(self, value):
        try:
            int(value)
            return True
        except:
            return False

    def isFloat(self, value):
        try:
            float(value)
            return True
        except:
            return False

    def check(self):
        try:
            tokens = self.lineEdit_nodeID.text().strip().split(',')
            try:
                tokens.remove('')
            except:     
                pass
            self.nodes_typed = list(map(int, tokens))
        except Exception:
            error("Wrong input for Node ID's!", "Error Node ID's")
            return

        try:
            for node in self.nodes_typed:
                self.nodes[node].external_index
        except:
            message = [" The Node ID input values must be\n major than 1 and less than {}.".format(len(self.nodes))]
            error(message[0], title = " INCORRECT NODE ID INPUT! ")
            return

        fx = fy = fz = 0.0
        if self.lineEdit_fx.text() != "":
            if self.isFloat(self.lineEdit_fx.text()):
                fx = float(self.lineEdit_fx.text())
            else:
                error("Wrong input (fx)!", "Error")
                return
        
        if self.lineEdit_fy.text() != "":
            if self.isFloat(self.lineEdit_fy.text()):
                fy = float(self.lineEdit_fy.text())
            else:
                error("Wrong input (fy)!", "Error")
                return

        if self.lineEdit_fz.text() != "":
            if self.isFloat(self.lineEdit_fz.text()):
                fz = float(self.lineEdit_fz.text())
            else:
                error("Wrong input (fz)!", "Error")
                return
        
        mx = my = mz = 0.0
        if self.lineEdit_mx.text() != "":
            if self.isFloat(self.lineEdit_mx.text()):
                mx = float(self.lineEdit_mx.text())
            else:
                error("Wrong input (mx)!", "Error")
                return
        
        if self.lineEdit_my.text() != "":
            if self.isFloat(self.lineEdit_my.text()):
                my = float(self.lineEdit_my.text())
            else:
                error("Wrong input (my)!", "Error")
                return

        if self.lineEdit_mz.text() != "":
            if self.isFloat(self.lineEdit_mz.text()):
                mz = float(self.lineEdit_mz.text())
            else:
                error("Wrong input (mz)!", "Error")
                return

        if fx==fy==fz==mx==my==mz==0.0:
            error("You must to prescribe at least one DOF to confirm the input!", title = " ERROR ")
            return

        self.loads = [fx, fy, fz, mx, my, mz]
        self.close()