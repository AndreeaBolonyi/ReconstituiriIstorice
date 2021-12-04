from domain.BoneModel import BoneModel
from domain.Response import Response
from ml_alorithms.DecisionTree import DecisionTree


class Repository:
    def __init__(self, ann):
        self.__client = None
        self.__bones = []
        self.__network = ann
        self.init_ui_data()
        self.tree = None

    def init_ui_data(self):
        bone1_map_model = {"HML": "", "HEB": "", "HHD": "", "HMLD": ""}
        bone2_map_model = {"FML": "", "FHD": "", "FEB": "", "FMLD": ""}
        bone1 = BoneModel("Humerus", bone1_map_model, "", "", "assets\\humerus.png", "info\\humerus_info.csv")
        bone2 = BoneModel("Femur", bone2_map_model, "", "", "assets\\femur.png", "info\\femur_info.csv")
        self.__bones.append(bone1)
        self.__bones.append(bone2)

    def get_bones(self):
        return self.__bones

    def get_bone_info(self, features, bone_type):
        bone = BoneModel(bone_type, features, "", "", "", "")
        self.tree = DecisionTree(bone)
        self.tree.solve_sex()
        sex, classes_name = self.tree.predict_one()
        sex = list(classes_name)[sex]

        self.tree.solve_age()
        age, classes_name = self.tree.predict_one()
        age = list(classes_name)[age]

        return Response(sex, age)

    def save_bone(self, bonePaylaod):
        sex = 0
        features = bonePaylaod.get_bone_features()
        if features["SEX"] == "female":
            sex = 1
        #TODO: De verificat daca osul exista in baza de date
        if bonePaylaod.get_bone_type() == "Humerus":
            with open('data/humerus.csv', 'a') as fd:
                fd.write(str(float(features["HML"])) + "," + str(float(features["HEB"])) + "," + str(
                    float(features["HHD"])) +
                         "," + str(float(features["HMLD"])) + "," + str(sex) + "," + str(features["AGE"]))
        if bonePaylaod.get_bone_type() == "Femur":
            with open('data/femur.csv', 'a') as fd:
                fd.write(str(float(features["FML"])) + "," + str(float(features["FHD"])) + "," + str(
                    float(features["FEB"])) +
                         "," + str(float(features["FMLD"])) + "," + str(sex) + "," + str(features["AGE"]))
