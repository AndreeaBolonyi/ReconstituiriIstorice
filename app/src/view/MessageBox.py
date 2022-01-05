from PySide6.QtWidgets import QMessageBox


class MessageBox:
    def __init__(self, errorType, msg):
        self.__msgBox = QMessageBox()
        self.__msgBox.setWindowTitle(errorType)
        self.__msgBox.setText(msg)

    def show(self):
        self.__msgBox.exec()