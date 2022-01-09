class Payload:
    def __init__(self, bone_type, features):
        self.__boneType = bone_type
        self.__features = features

    def get_bone_type(self):
        return self.__boneType

    def get_bone_features(self):
        return self.__features
