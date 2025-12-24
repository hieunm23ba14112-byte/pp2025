from domains.Student import Student
from domains.Course import Course
from domains.Mark import Mark
from datetime import datetime
from pathlib import Path
import numpy as np


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

    def get_students(self):
        return list(self.__students)

    def get_courses(self):
        return list(self.__courses)

    def get_marks(self):
        return list(self.__marks)
    
    def get_students_sorted_by_gpa(self):
        self.count_gpa_for_all_student()
        return sorted(self.__students, key=lambda s: s.get_gpa(), reverse=True)
        
    def get_students_sorted_by_gpa_data(self):
        self.count_gpa_for_all_student()
        students = sorted(self.__students, key=lambda s: s.get_gpa(), reverse=True)
        
        stu_list = []
        
        for stu in students:
            stu_list.append({
                "id" : stu.get_id(),
                "name" : stu.get_name(),
                "gpa" : stu.get_gpa()
            })
            
        return stu_list
    
    def get_courses_data(self):
        courses = []
        for course in self.__courses:
            courses.append({
                "id": course.get_id(),
                "name": course.get_name(),
            })
        return courses

    def get_students_data(self):
        students = []
        for stu in self.__students:
            students.append({
                "id": stu.get_id(),
                "name": stu.get_name(),
                "dob": stu.get_dob(),
            })
        return students

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
            
    def write_students_to_file(self, path="students.txt"):
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(len(self.__students)) + "\n")
            for s in self.__students:
                f.write(s.get_id() + "\n")
                f.write(s.get_name() + "\n")
                f.write(s.get_dob() + "\n")
                
    def write_courses_to_file(self, path="courses.txt"):
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(len(self.__courses)) + "\n")
            for c in self.__courses:
                f.write(c.get_id() + "\n")
                f.write(c.get_name() + "\n")
                
    def write_marks_to_file(self, path="mark.txt"):
        with open(path, "w", encoding="utf-8") as f:
            for m in self.__marks:
                f.write(m.get_course_id() + "\n")
                for sid, scores in m.get_marks().items():
                    for score in scores:
                        f.write(f"{sid} {score}\n")
                f.write("\n")

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
        
    def inputAll(self):
        self.inputStudents()
        self.inputCourses()
        self.inputMarks()

    def read_students_from_file(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        n = int(lines[0])
        idx = 1
        for _ in range(n):
            sid = lines[idx]; idx += 1
            name = lines[idx]; idx += 1
            dob = lines[idx]; idx += 1
            self.__students.append(Student(sid, name, dob))

    def read_courses_from_file(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        n = int(lines[0])
        idx = 1
        for _ in range(n):
            cid = lines[idx]; idx += 1
            name = lines[idx]; idx += 1
            self.__courses.append(Course(cid, name))

    def read_marks_from_file(self, path: str, default_credit: int = 1):
        """
        Format marks.txt:
        MATH01
        STU01 8.5
        STU02 7.0
        <Some newline>
        ICT01
        STU01 8.0
        ...
        """
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        current_mark_obj = None
        for line in lines:
            parts = line.split()
            if len(parts) == 1:
                # dòng course id mới
                cid = parts[0]
                current_mark_obj = Mark(cid)
                self.__marks.append(current_mark_obj)
            elif len(parts) == 2 and current_mark_obj is not None:
                sid, mark_str = parts
                try:
                    m_val = float(mark_str)
                except ValueError:
                    continue
                current_mark_obj.add_mark(sid, m_val)
                current_mark_obj.add_credit(sid, default_credit)

    def load_from_files(self,
                        students_path: str = "./input_data/students.txt",
                        courses_path: str = "./input_data/courses.txt",
                        marks_path: str = "./input_data/mark.txt"):
        """Load data files.

        If given relative paths, resolve them against the project root (the directory above `pw4/`).
        This makes it work whether you run from `pw4/` or from the repo root.
        """
        base_dir = Path(__file__).resolve().parents[2]  # .../pp2025

        sp = Path(students_path)
        cp = Path(courses_path)
        mp = Path(marks_path)

        if not sp.is_absolute():
            sp = base_dir / sp
        if not cp.is_absolute():
            cp = base_dir / cp
        if not mp.is_absolute():
            mp = base_dir / mp

        self.read_students_from_file(str(sp))
        self.read_courses_from_file(str(cp))
        self.read_marks_from_file(str(mp))
