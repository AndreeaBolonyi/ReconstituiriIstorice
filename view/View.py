import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QMessageBox, QLabel, QPushButton, QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget

from controller.Controller import Controller
from domain.Payload import Payload
from view.MessageBox import MessageBox
from view.ResponseWindow import ResponseWindow


class View(QWidget):
    def __init__(self,controller):
        self.__controller = controller
        self.__init_GUI()

    def __init_GUI(self):
        super().__init__()
        self.resize(200, 250)
        self.setWindowTitle("Reconstituiri istorice")

        self.__label_introdu = QLabel("Introdu caracteristicile:",alignment=QtCore.Qt.AlignCenter)

        self.__button_send = QPushButton("Trimite")
        self.__button_send.clicked.connect(self.__buttonSendClicked)

        self.__label_type = QLabel("Tip: ")
        self.__label_length = QtWidgets.QLabel("Lungime (cm): ")

        self.__textBox_length = QLineEdit()
        self.__comboBox_type = QComboBox()

        self.__comboBox_type.addItems(self.__controller.get_bone_types())

        self.__vBox_labels = QVBoxLayout(alignment=QtCore.Qt.AlignLeft)
        self.__vBox_inputs = QVBoxLayout(alignment=QtCore.Qt.AlignLeft)
        self.__vBox_labels.setSpacing(20)
        self.__vBox_inputs.setSpacing(20)

        self.__vBox_labels.addWidget(self.__label_type)
        self.__vBox_labels.addWidget(self.__label_length)

        self.__vBox_inputs.addWidget(self.__comboBox_type)
        self.__vBox_inputs.addWidget(self.__textBox_length)

        self.__hBox_inputs = QHBoxLayout()
        self.__hBox_inputs.addLayout(self.__vBox_labels)
        self.__hBox_inputs.addLayout(self.__vBox_inputs)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(40)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.layout.addWidget(self.__label_introdu)
        self.layout.addLayout(self.__hBox_inputs)
        self.layout.addWidget(self.__button_send)

    def __buttonSendClicked(self):
        length = self.__textBox_length.text()
        try:
            length = float(length)
        except ValueError:
            MessageBox("Eroare","Lungimea trebuie sa fie un numar!").show()
            return
        if length <= 0:
            MessageBox("Eroare", "Lungimea trebuie sa fie mai mare decat 0!").show()
            return
        bone_info = Payload(self.__comboBox_type.currentText(),length)
        self.__respWindow = ResponseWindow(self.__controller,bone_info,self.__controller.process_bone_info(bone_info))
        self.__respWindow.show()







