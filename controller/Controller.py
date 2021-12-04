class Controller:
    def __init__(self, service):
        self.__service = service

    def process_bone_info(self, bone_info):
        return self.__service.get_bone_info(bone_info.get_bone_features(), bone_info.get_bone_type())

    def get_bone_types(self):
        return self.__service.get_bone_types()

    def get_bone_info_by_type(self, bone_type):
        return self.__service.get_bone_info_by_type(bone_type)

    def run3DRendering(self, bone_info):
        pass

    def save_bone(self,bonePayload):
        self.__service.save_bone(bonePayload)
