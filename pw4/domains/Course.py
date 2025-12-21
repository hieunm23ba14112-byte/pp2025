class Course:
    def __init__(self, cid, name):
        self.__id = cid
        self.__name = name

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name