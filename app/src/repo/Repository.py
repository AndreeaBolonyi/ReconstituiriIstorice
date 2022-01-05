from app.src.domain.BoneModel import BoneModel
from app.src.domain.Response import Response
from app.ai.ml_algorithms.DecisionTree import DecisionTree

from csv import reader


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
        bone1 = BoneModel("Humerus", bone1_map_model, "", "", "app\\assets\\humerus.png", "app\\ai\\info\\humerus_info.csv")
        bone2 = BoneModel("Femur", bone2_map_model, "", "", "app\\assets\\femur.png", "app\\ai\\info\\femur_info.csv")
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

    def save_bone(self, bonePayload):
        if self.bone_exists(bonePayload):
            return
        sex = 0
        features = bonePayload.get_bone_features()
        if features["SEX"] == "female":
            sex = 1
        keys = list(features.keys())
        with open('app/data/'+bonePayload.get_bone_type().lower()+'.csv', 'a') as fd:
            line = ""
            for i in range(len(keys) - 2):
                line += str(float(features[keys[i]])) + ","
            line += str(sex) + "," + str(features["AGE"]) + "\n"
            fd.write(line)

    def bone_exists(self,bonePayload):
        features = bonePayload.get_bone_features()
        keys = list(features.keys())
        with open('app/data/'+bonePayload.get_bone_type().lower()+'.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                exista = True
                for i in range(len(keys)-2):
                    if row[i] != str(float(features[keys[i]])):
                        exista = False
                if exista:
                    return True
        return False
