from domain.Response import Response


class Repository:
    def __init__(self, ann):
        self.__client = None
        self.__bone_types = ["Left Humerus", "Right Humerus", "Rib", "Radius", "Carpals", "Metacarpals", "Phalanges"]
        self.__network = ann

    def get_bone_types(self):
        return self.__bone_types

    def get_bone_info(self, length, bone_type):
        return Response("M",100)
