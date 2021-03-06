class BoneModel:
    def __init__(self, bone_type, features, sex, age, image, infoFile):
        self.__bone_type = bone_type
        self.__features = features
        self.__sex = sex
        self.__age = age
        self.image = image
        self.infoFile = infoFile

    def get_bone_type(self):
        return self.__bone_type

    def get_features(self):
        return self.__features

    def get_sex(self):
        return self.__sex

    def get_age(self):
        return self.__age

    def get_feature_value(self, feature):
        return self.__features[feature]
