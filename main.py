import sys

from controller.Controller import Controller
from domain.Payload import Payload
from repo.Repository import Repository
from service.Service import Service
from view.View import View
from PySide6 import QtCore, QtWidgets, QtGui
import sys

if __name__ == '__main__':
    repository = Repository(None)
    service = Service(repository)
    controller = Controller(service)

    app = QtWidgets.QApplication([])
    view = View(controller)
    view.show()

    sys.exit(app.exec())
