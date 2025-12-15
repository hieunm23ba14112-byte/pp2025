from .student import Student
from .course import Course
from .mark import Mark

class SystemManageMark:
    def __init__(self, students=None, courses=None):
        self.students = students if students else []
        self.courses = courses if courses else []
        # Keep old attribute names for compatibility
        self.studentList = self.students
        self.courseList = self.courses

    def add_student(self, s):
        self.studentList.append(s)

    def add_course(self, c):
        self.courseList.append(c)

    def get_student(self, sid):
        for s in self.studentList:
            if s.id == sid:
                return s
        return None

    def get_course(self, cid):
        for c in self.courseList:
            if c.id == cid:
                return c
        return None

    def add_mark(self, sid, cid, mark, credits):
        student = self.get_student(sid)
        course = self.get_course(cid)

        if not student or not course:
            return

        mark_obj = Mark(mark, credits, cid)
        student.add_mark(mark_obj)
        course.add_student(student)
