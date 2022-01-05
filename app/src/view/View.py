import csv
from functools import partial

from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QPushButton, QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox
from app.src.domain.Payload import Payload
from app.src.domain.validators.FemurValidator import FemurValidator
from app.src.domain.validators.HumerusValidator import HumerusValidator
from app.src.utils.utils import get_list_of_values
from app.src.view.MessageBox import MessageBox
from app.src.view.ResponseWindow import ResponseWindow


class View(QWidget):
    def __init__(self, controller):
        self.__controller = controller
        self.__init_GUI()
        self.__validators = {}
        self.__init_validators()

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
        self.__features = self.__current_bone.get_features()
        self.__labels = {}
        self.__inputs = {}
        self.__info_buttons = {}
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

        self.__features_info = {}
        self.__read_features_info()

        self.__comboBox_type.currentTextChanged.connect(self.__on_selection_change_from_comboBox_type)

        self.__hBox_inputs = QHBoxLayout()
        self.__hBox_inputs.addLayout(self.__vBox_labels)
        self.__hBox_inputs.addLayout(self.__vBox_inputs)
        self.__hBox_inputs.setSpacing(10)

        self.__left_layout = QVBoxLayout()
        self.__left_layout.setSpacing(30)

        self.__checkBox_salvare_date = QCheckBox("Adaugare informatii in baza de date a\naplicatiei pentru imbunatatirea\nperformantei")
        self.__checkBox_salvare_date.setChecked(True)

        self.__left_layout.addWidget(self.__label_introdu)
        self.__left_layout.addLayout(self.__hBox_inputs)
        self.__left_layout.addWidget(self.__checkBox_salvare_date)
        self.__left_layout.addWidget(self.__button_send)

        self.layout = QHBoxLayout(self)
        self.layout.addLayout(self.__left_layout)
        self.layout.addWidget(self.__image)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)

    def __generate_labels_and_inputs(self):
        self.__labels = {}
        self.__inputs = {}
        self.__info_buttons = {}
        for f in self.__features:
            self.__labels[f] = QtWidgets.QLabel(f + " (mm) :")
            self.__inputs[f] = QLineEdit()
            self.__info_buttons[f] = QPushButton("Info")
            self.__info_buttons[f].setFixedWidth(30)
            self.__info_buttons[f].clicked.connect(partial(self.__info_button_clicked,f))



    def __add_labels_and_inputs(self):
        for l in self.__labels:
            self.__vBox_labels.addWidget(self.__labels[l])
        for i in self.__inputs:
            hBox = QHBoxLayout()
            hBox.addWidget(self.__inputs[i])
            hBox.addWidget(self.__info_buttons[i])
            hBox.setSpacing(10)
            self.__vBox_inputs.addLayout(hBox)
        self.setFixedHeight(250+40*len(self.__labels))

    def __delete_labels_and_inputs(self):
        for f in self.__labels:
            lbl = self.__labels[f]
            inp = self.__inputs[f]
            btn = self.__info_buttons[f]
            self.__vBox_labels.removeWidget(lbl)
            lbl.deleteLater()
            lbl = None
            self.__hBox_inputs.removeWidget(inp)
            inp.deleteLater()
            inp = None
            self.__hBox_inputs.removeWidget(btn)
            btn.deleteLater()
            btn = None
        for i in range(1,self.__vBox_inputs.count()):
            item = self.__vBox_inputs.itemAt(1)
            self.__vBox_inputs.removeItem(item)
            lt = item.layout()
            lt.deleteLater()
            lt = None

    def __on_selection_change_from_comboBox_type(self):
        self.__delete_labels_and_inputs()
        self.__current_bone = self.__controller.get_bone_info_by_type(self.__comboBox_type.currentText())
        self.__read_features_info()
        self.__features = self.__current_bone.get_features()
        self.__generate_labels_and_inputs()
        self.__add_labels_and_inputs()
        self.__set_image(self.__current_bone.image)

    def __set_image(self,image):
        self.__image.setPixmap(QPixmap(image).scaledToHeight(self.height()-40))
        self.setFixedWidth(280+self.__image.pixmap().width())

    def __info_button_clicked(self, feature):
        MessageBox("Info", self.__features_info[feature]).show()

    def __read_features_info(self):
        self.__features_info = {}
        file = open(self.__current_bone.infoFile)
        csvreader = csv.reader(file)
        for row in csvreader:
            self.__features_info[row[0]] = row[1]
        file.close()

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
        try:
            self.__validators[self.__comboBox_type.currentText()].validate(*get_list_of_values(values))
        except Exception as exception:
            MessageBox("Eroare", str(exception)).show()
            return

        bone_info = Payload(self.__comboBox_type.currentText(), values)
        response = self.__controller.process_bone_info(bone_info)
        self.__respWindow = ResponseWindow(self.__controller, bone_info, response)
        self.__respWindow.show()
        self.__clear_inputs()

        if self.__checkBox_salvare_date.isChecked():
            values["SEX"] = response.get_sex()
            values["AGE"] = response.get_age()
            response_bone = Payload(self.__comboBox_type.currentText(), values)
            self.__controller.save_bone(response_bone)


    def __clear_inputs(self):
        for i in self.__inputs:
            self.__inputs[i].clear()

    def __init_validators(self):
        bone_types = self.__controller.get_bone_types()
        for type in bone_types:
            if type == "Humerus":
                self.__validators["Humerus"] = HumerusValidator()
            elif type == "Femur":
                self.__validators["Femur"] = FemurValidator()


