import numpy as np, math

class Mark:
    def __init__(self, cid):
        self.__courseId = cid
        self.__marks = {}     # {sid: [marks]}
        self.__credits = {}   # {sid: [credits]}

    def add_mark(self, sid, mark):
        mark = math.floor(mark * 10) / 10
        self.__marks.setdefault(sid, []).append(mark)

    def add_credit(self, sid, credit):
        self.__credits.setdefault(sid, []).append(credit)

    def get_gpa_sid(self, sid):
        if sid not in self.__marks or sid not in self.__credits:
            return 0.0

        marks = np.array(self.__marks[sid])
        credits = np.array(self.__credits[sid])

        gpa = np.sum(marks * credits) / np.sum(credits)
        
        return round(gpa, 1)
    
    def get_course_id(self):
        return self.__courseId

    def get_marks(self):
        return self.__marks