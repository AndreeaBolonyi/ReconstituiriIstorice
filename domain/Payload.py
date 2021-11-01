class Payload:
    def __init__(self, bone_type, bone_length):
        self.__boneType = bone_type
        self.__boneLength = bone_length

    def get_bone_type(self):
        return self.__boneType

    def get_bone_length(self):
        return self.__boneLength
