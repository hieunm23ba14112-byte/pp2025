from datetime import datetime
import math, numpy as np 

class Student:
    def __init__(self, sid, name, dob):
        self.__id = sid
        self.__name = name
        self.__dob = dob
        self.__gpa = 0

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob
    
    def get_gpa(self):
        return self.__gpa

    def set_gpa(self, gpa):
        self.__gpa = gpa

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
    

class SystemManagementMark:
    def __init__(self):
        self.__students = []
        self.__courses = []
        self.__marks = []
        
    def count_gpa_for_all_student(self):
        for stu in self.__students:
            total_marks = []
            total_credits = []

            for m in self.__marks:
                sid = stu.get_id()
                if sid in m._Mark__marks and sid in m._Mark__credits:
                    total_marks.extend(m._Mark__marks[sid])
                    total_credits.extend(m._Mark__credits[sid])

            if total_credits:
                marks = np.array(total_marks)
                credits = np.array(total_credits)
                gpa = np.sum(marks * credits) / np.sum(credits)
                stu.set_gpa(round(gpa, 1))
            else:
                stu.set_gpa(0.0)

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
            credit = int(input("  Credit: "))
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
                mark.add_credit(stu.get_id(), credit)

            self.__marks.append(mark)


    def showStudents(self):
        print("\n===== STUDENT LIST =====")
        print("-" * 60)
        print(f"{'No':>3} | {'ID':12} | {'Name':20} | {'DoB':>10}")
        print("-" * 60)

        for i, s in enumerate(self.__students, start=1):
            print(f"{i:3} | {s.get_id():12} | {s.get_name():20} | {s.get_dob():>10}")

    def showStudentsGpa(self):
        print("\n===== STUDENT GPA LIST =====")
        print("-" * 50)
        print(f"{'No':<4} | {'Student ID':<12} | {'Name':<20} | {'GPA':>5}")
        print("-" * 50)

        for i, s in enumerate(self.__students, start=1):
            print(f"{i:<4} | {s.get_id():<12} | {s.get_name():<20} | {s.get_gpa():>5.1f}")

        print("-" * 50)

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

                score_str = ", ".join(f"{s:.1f}" for s in score)
                print(f"{sid:12} | {stu_name:<20} | {score_str}")
    
    def showCourses(self):
        print("\n===== COURSE LIST =====")
        print("-" * 60)
        print(f"{'No':>3} | {'Course ID':12} | {'Course Name':30}")
        print("-" * 60)

        for i, c in enumerate(self.__courses, start=1):
            print(f"{i:3} | {c.get_id():12} | {c.get_name():30}")


    def showStudentGpaDescending(self):
        self.__students.sort(key=lambda s: s.get_gpa(), reverse=True)
        self.showStudentsGpa()
                
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
    system.count_gpa_for_all_student()
    system.showStudentGpaDescending()
    system.showAll()

    
