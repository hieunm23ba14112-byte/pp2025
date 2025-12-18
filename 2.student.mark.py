from datetime import datetime

class Student:
    def __init__(self, sid, name, dob):
        self.__id = sid
        self.__name = name
        self.__dob = dob

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob


class Course:
    def __init__(self, cid, name):
        self.__id = cid
        self.__name = name

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name


class Mark:
    def __init__(self, cid):
        self.__courseId = cid
        self.__marks = {}  

    def add_mark(self, sid, mark):
        self.__marks[sid] = mark

    def get_course_id(self):
        return self.__courseId

    def get_marks(self):
        return self.__marks


class SystemManagementMark:
    def __init__(self):
        self.__students = []
        self.__courses = []
        self.__marks = []

    def isStudentId(self, sid):
        return sid.isalnum() and len(sid) >= 5

    def isStudentName(self, name):
        return name.strip() != "" and all(c.isalpha() or c.isspace() for c in name)

    def isStudentDob(self, dob):
        try:
            datetime.strptime(dob, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def isCourseId(self, cid):
        return cid.isalnum()

    def isCourseName(self, name):
        return name.strip() != ""

    def inputStudents(self):
        n = int(input("Number of students: "))
        for i in range(n):
            print(f"\nStudent {i+1}")
            sid = input("  Id: ")
            while not self.isStudentId(sid):
                sid = input("  Invalid Id: ")

            name = input("  Name: ")
            while not self.isStudentName(name):
                name = input("  Invalid Name: ")

            dob = input("  DoB (dd/mm/yyyy): ")
            while not self.isStudentDob(dob):
                dob = input("  Invalid DoB: ")

            self.__students.append(Student(sid, name, dob))

    def inputCourses(self):
        n = int(input("Number of courses: "))
        for i in range(n):
            print(f"\nCourse {i+1}")
            cid = input("  Course Id: ")
            while not self.isCourseId(cid):
                cid = input("  Invalid Course Id: ")

            name = input("  Course Name: ")
            while not self.isCourseName(name):
                name = input("  Invalid Course Name: ")

            self.__courses.append(Course(cid, name))

    def inputMarks(self):
        for course in self.__courses:
            print(f"\nMarks for course {course.get_id()} - {course.get_name()}")
            mark = Mark(course.get_id())

            for stu in self.__students:
                while True:
                    try:
                        m = float(input(f"  {stu.get_id()}: "))
                        if 0 <= m <= 10:
                            break
                    except ValueError:
                        pass
                mark.add_mark(stu.get_id(), m)

            self.__marks.append(mark)

    def showStudents(self):
        print("\n===== STUDENT LIST =====")
        for i, s in enumerate(self.__students, start=1):
            print(f"{i}. ID: {s.get_id()}, Name: {s.get_name()}, DoB: {s.get_dob()}")


    def showCourses(self):
        print("\n===== COURSE LIST =====")
        for i, c in enumerate(self.__courses, start=1):
            print(f"{i}. ID: {c.get_id()}, Name: {c.get_name()}")


    def showMarks(self):
        print("\n===== MARK LIST =====")

        for m in self.__marks:
            course_name = ""
            for c in self.__courses:
                if c.get_id() == m.get_course_id():
                    course_name = c.get_name()
                    break

            print(f"\nCourse: {m.get_course_id()} - {course_name}")
            print("-" * 40)

            for sid, score in m.get_marks().items():
                stu_name = ""
                for s in self.__students:
                    if s.get_id() == sid:
                        stu_name = s.get_name()
                        break

                print(f"{sid:12} | {stu_name:<20} | {score:5.2f}")

                
    def readAllInput(self):
        self.inputStudents()
        self.inputCourses()
        self.inputMarks()
        
    def showAll(self):
        self.showStudents()
        self.showCourses()
        self.showMarks()        
        
                
if __name__ == "__main__":
    system = SystemManagementMark()
    system.readAllInput()
    system.showAll()
    
