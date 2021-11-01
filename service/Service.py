class Service:
    def __init__(self, repository):
        self.__repository = repository

    def get_bone_types(self):
        return self.__repository.get_bone_types()

    def get_bone_info(self, bone_length,bone_type):
        return self.__repository.get_bone_info(bone_length, bone_type)
