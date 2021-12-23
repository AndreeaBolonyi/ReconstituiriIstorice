from controller.Controller import Controller
from domain.BoneModel import BoneModel
from ml_alorithms.DecisionTree import DecisionTree
from repo.Repository import Repository
from service.Service import Service
from view.View import View
from PySide6 import QtWidgets
import sys

bone1 = BoneModel("Humerus", {'HML': 286, 'HEB': 65, 'HHD': 42.45, 'HMLD': 21.82, 'SEX': 0, 'AGE': '40-50'},
                  'male', '40-50', "", "")
# bone2 = BoneModel("Humerus", {'HML': 282,'HEB': 49, 'HHD': 36.99,'HMLD': 20.73, 'SEX': 1,'AGE': "50+"},
#                       'female', "50+", "", "")
# bone3 = BoneModel("Femur", {"FML": "386", "FHD": "70", "FEB": "39.65", "FMLD": "22.58"}, 'female', '50+', "", "")

if __name__ == '__main__':
    repository = Repository(None)
    service = Service(repository)
    controller = Controller(service)

    app = QtWidgets.QApplication([])
    view = View(controller)
    view.show()

    decision_tree = DecisionTree(bone1)
    decision_tree.statistical_analysis()

    sys.exit(app.exec())
