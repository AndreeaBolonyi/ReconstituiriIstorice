class Response:
    def __init__(self, sex, age):
        self.__sex = sex
        self.__age = age

    def get_sex(self):
        return self.__sex

    def get_age(self):
        return self.__age