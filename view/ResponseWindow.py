from PySide6 import QtCore
from PySide6.QtWidgets import QMessageBox, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton

from domain.Response import Response

class ResponseWindow(QWidget):
    def __init__(self,controller,bone_info,response):
        super().__init__()
        self.__controller = controller
        self.__bone_info = bone_info
        self.__response = response
        self.__init_GUI()

    def __init_GUI(self):
        self.resize(200, 200)
        self.setWindowTitle("Reconstituiri istorice")

        self.__label_result = QLabel("Rezultat", alignment=QtCore.Qt.AlignCenter)

        self.__vBox_features = QVBoxLayout(alignment=QtCore.Qt.AlignLeft)
        self.__vBox_values = QVBoxLayout(alignment=QtCore.Qt.AlignLeft)
        self.__vBox_features.setSpacing(20)
        self.__vBox_values.setSpacing(20)

        self.__label_sex = QLabel("Sex: ")
        self.__label_age = QLabel("Varsta: ")

        self.__label_sex_value = QLabel(str(self.__response.get_sex()))
        self.__label_age_value = QLabel(str(self.__response.get_age()))

        self.__vBox_features.addWidget(self.__label_sex)
        self.__vBox_features.addWidget(self.__label_age)

        self.__vBox_values.addWidget(self.__label_sex_value)
        self.__vBox_values.addWidget(self.__label_age_value)

        self.__hBox_response = QHBoxLayout()
        self.__hBox_response.addLayout(self.__vBox_features)
        self.__hBox_response.addLayout(self.__vBox_values)

        self.__button_ok = QPushButton("OK")
        self.__button_ok.clicked.connect(self.__buttonOkClicked)

        self.__button_view3d = QPushButton("Vezi 3D")
        self.__button_view3d.clicked.connect(self.__buttonView3dClicked)

        self.__hBox_buttons = QHBoxLayout()
        self.__hBox_buttons.addWidget(self.__button_ok)
        self.__hBox_buttons.addWidget(self.__button_view3d)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(40)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.addWidget(self.__label_result)
        self.layout.addLayout(self.__hBox_response)
        self.layout.addLayout(self.__hBox_buttons)

    def __buttonOkClicked(self):
        self.close()

    def __buttonView3dClicked(self):
        self.__controller.run3DRendering(self.__bone_info)
