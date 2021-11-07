import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox, QLabel, QPushButton, QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget

from controller.Controller import Controller
from domain.Payload import Payload
from view.MessageBox import MessageBox
from view.ResponseWindow import ResponseWindow


class View(QWidget):
    def __init__(self, controller):
        self.__controller = controller
        self.__init_GUI()

    def __init_GUI(self):
        super().__init__()

        self.setWindowTitle("Reconstituiri istorice")

        self.__label_introdu = QLabel("Introdu caracteristicile:", alignment=QtCore.Qt.AlignCenter)

        self.__button_send = QPushButton("Trimite")
        self.__button_send.clicked.connect(self.__buttonSendClicked)

        self.__label_type = QLabel("Tip: ")

        self.__comboBox_type = QComboBox()
        self.__comboBox_type.addItems(self.__controller.get_bone_types())

        self.__current_bone = self.__controller.get_bone_info_by_type(self.__comboBox_type.currentText())
        self.__features = self.__current_bone.get_feature()
        self.__labels = {}
        self.__inputs = {}
        self.__generate_labels_and_inputs()

        self.__vBox_labels = QVBoxLayout(alignment=QtCore.Qt.AlignLeft)
        self.__vBox_inputs = QVBoxLayout(alignment=QtCore.Qt.AlignLeft)
        self.__vBox_labels.setSpacing(20)
        self.__vBox_inputs.setSpacing(20)

        self.__vBox_labels.addWidget(self.__label_type)
        self.__vBox_inputs.addWidget(self.__comboBox_type)
        self.__add_labels_and_inputs()

        self.__image = QLabel()
        self.__set_image(self.__current_bone.image)

        self.__comboBox_type.currentTextChanged.connect(self.__on_selection_change_from_comboBox_type)

        self.__hBox_inputs = QHBoxLayout()
        self.__hBox_inputs.addLayout(self.__vBox_labels)
        self.__hBox_inputs.addLayout(self.__vBox_inputs)

        self.__left_layout = QVBoxLayout()
        self.__left_layout.setSpacing(40)

        self.__left_layout.addWidget(self.__label_introdu)
        self.__left_layout.addLayout(self.__hBox_inputs)
        self.__left_layout.addWidget(self.__button_send)

        self.layout = QHBoxLayout(self)
        self.layout.addLayout(self.__left_layout)
        self.layout.addWidget(self.__image)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)



    def __generate_labels_and_inputs(self):
        self.__labels = {}
        self.__inputs = {}
        for f in self.__features:
            self.__labels[f] = QtWidgets.QLabel(f + ":")
            self.__inputs[f] = QLineEdit()

    def __add_labels_and_inputs(self):
        for l in self.__labels:
            self.__vBox_labels.addWidget(self.__labels[l])
        for i in self.__inputs:
            self.__vBox_inputs.addWidget(self.__inputs[i])
        self.setFixedHeight(180+40*len(self.__labels))
        #self.setFixedWidth(350)

    def __delete_labels_and_inputs(self):
        for f in self.__labels:
            lbl = self.__labels[f]
            inp = self.__inputs[f]
            self.__vBox_labels.removeWidget(lbl)
            lbl.deleteLater()
            lbl = None
            self.__vBox_inputs.removeWidget(inp)
            inp.deleteLater()
            inp = None

    def __on_selection_change_from_comboBox_type(self):
        self.__delete_labels_and_inputs()
        self.__current_bone = self.__controller.get_bone_info_by_type(self.__comboBox_type.currentText())
        self.__features = self.__current_bone.get_feature()
        self.__generate_labels_and_inputs()
        self.__add_labels_and_inputs()
        print(self.height() - 50)
        self.__set_image(self.__current_bone.image)

    def __set_image(self,image):
        self.__image.setPixmap(QPixmap(image).scaledToHeight(self.height()-40))
        self.setFixedWidth(220+self.__image.pixmap().width())

    def __buttonSendClicked(self):
        values = {}
        err = ""
        for f in self.__features:
            val = self.__inputs[f].text()
            try:
                values[f] = float(val)
            except ValueError:
                err += f + " trebuie sa fie numar!\n"
                continue
            if values[f] <= 0:
                err += f + " trebuie sa fie mai mare decat 0!\n"
        if err != "":
            MessageBox("Eroare", err).show()
            return
        bone_info = Payload(self.__comboBox_type.currentText(), values)
        self.__respWindow = ResponseWindow(self.__controller, bone_info, self.__controller.process_bone_info(bone_info))
        self.__respWindow.show()
