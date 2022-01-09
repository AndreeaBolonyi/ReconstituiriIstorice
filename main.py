from app.src.controller import Controller
from app.ai.ml_algorithms import DecisionTree
from app.src.repo.Repository import Repository
from app.src.service.Service import Service
from app.src.view import View
from PySide6 import QtWidgets
from app.src.domain import BoneModel
import sys


# bone2 = BoneModel("Humerus", {'HML': 282,'HEB': 49, 'HHD': 36.99,'HMLD': 20.73, 'SEX': 1,'AGE': "50+"},
#                       'female', "50+", "", "")
# bone3 = BoneModel("Femur", {"FML": "386", "FHD": "70", "FEB": "39.65", "FMLD": "22.58"}, 'female', '50+', "", "")

if __name__ == '__main__':
    bone1 = BoneModel.BoneModel("Humerus", {'HML': 286, 'HEB': 65, 'HHD': 42.45, 'HMLD': 21.82, 'SEX': 0, 'AGE': '40-50'},
                      'male', '40-50', "", "")

    repository = Repository(None)
    service = Service(repository)
    controller = Controller.Controller(service)

    app = QtWidgets.QApplication([])
    view = View.View(controller)
    view.show()

    decision_tree = DecisionTree.DecisionTree(bone1)
    decision_tree.plot_statistical_anaylisis_ann_tree()

    sys.exit(app.exec())
