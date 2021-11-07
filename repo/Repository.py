from domain.BoneModel import BoneModel
from domain.Response import Response


class Repository:
    def __init__(self, ann):
        self.__client = None
        self.__bone_types = []
        self.__network = ann

    def init_ui_data(self):
        bone1_map_model = {"ml": "", "hd": "", "eb": ""}
        bone2_map_model = {"ml": "", "hd": "", "eb": ""}
        bone1 = BoneModel("Humerus", bone1_map_model, "", "", "humerus.png")
        bone2 = BoneModel("Femur", bone2_map_model, "", "", "femur.jpg")
        self.__bone_types.append(bone1)
        self.__bone_types.append(bone2)

    def get_bone_types(self):
        return self.__bone_types

    def get_bone_info(self, features, bone_type):
        return Response("M", 100)
