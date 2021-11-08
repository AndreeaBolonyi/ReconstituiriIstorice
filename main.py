from controller.Controller import Controller
from repo.Repository import Repository
from service.Service import Service
from view.View import View
from PySide6 import QtWidgets
import sys


if __name__ == '__main__':
    repository = Repository(None)
    service = Service(repository)
    controller = Controller(service)

    app = QtWidgets.QApplication([])
    view = View(controller)
    view.show()
    # bone = BoneModel("humerus", {'HML': 286, 'HEB': 65, 'HHD': 42.45, 'HMLD': 21.82, 'SEX': 0, 'AGE': '40-50'},
    #                       'male', '40-50', "")
    # bone = BoneModel("humerus", {'HML': 282,'HEB': 49, 'HHD': 36.99,'HMLD': 20.73, 'SEX': 1,'AGE': "50+"},
    #                       'female', "50+", "")

    sys.exit(app.exec())
