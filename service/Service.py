class Service:
    def __init__(self, repository):
        self.__repository = repository

    def get_bones(self):
        return self.__repository.get_bones()

    def get_bone_info(self, features, bone_type):
        return self.__repository.get_bone_info(features, bone_type)

    def get_bone_types(self):
        bone_types_list = []
        bones = self.__repository.get_bones()
        for bone in bones:
            bone_types_list.append(bone.get_bone_type())
        return bone_types_list

    def get_bone_info_by_type(self, bone_type):
        bones = self.__repository.get_bones()
        for bone in bones:
            if bone.get_bone_type() == bone_type:
                return bone
