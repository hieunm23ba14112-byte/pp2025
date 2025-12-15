# Too lazy, so i put data in files
# I need a better structure for student mark management
# What is the best???
 

import math, curses
import numpy as np

class Mark:
    def __init__(self, cid, mark, credits):
        self.courseId = cid
        self.mark = float(mark)
        self.credits = int(credits)
        
    def __str__(self):
        return f"{self.mark} in course {self.courseId}"

    
class Student:
    def __init__(self, id, name, dob):
        self.id = id
        self.name = name
        self.dob = dob
        self.courses = []
        self.marks = []   
        
    def __str__(self):
        return "Student "+ self.name + " (" + self.id + ", " + self.dob + ")"
    
    def addMark(self, mark):
        self.marks.append(mark)
        self.courses.append(mark.courseId)
    
    def getGPA(self):
        if len(self.marks) == 0:
            return 0.0
        
        totalCredits = 0
        totalMark = 0.0
        
        for mark in self.marks:
            totalMark += mark.mark * mark.credits
            totalCredits += mark.credits 
            
        return totalMark / totalCredits
        
class Course:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.students = []
        
    def addStu(self, sid):
        self.students.append(sid)
        
    def __str__(self):
        return "Course " + self.name + " (" + self.id + ")"
        
class System:
    def __init__(self, name = "Dark"):
        self.name = name
        self.students = []
        self.courses = []
        self.readDataFromFiles()
      
        
    def readCourses(self, inputPath):
        with open(inputPath, "r") as f:
            lines = f.read().splitlines()
            
        for line in lines:
            id, name = line.split("|")
            self.courses.append(Course(id, name))

        print(f'[*] Add courses from "{inputPath}" into System {self.name} complete !!!')        
        return 
    
    def readStudents(self, inputPath):
        with open(inputPath, "r") as f:
            lines = f.read().splitlines()
            
        for line in lines:
            id, name, dob = line.split("|")
            self.students.append(Student(id, name, dob))

        print(f'[*] Add students from "{inputPath}" into System {self.name} complete !!!')        
        return 
    
    def haveCourseId(self, cid):
        for course in self.courses:
            if cid == course.id:
                return course
            
        return None
    
    def haveStuId(self, sid):
        for stu in self.students:
            if sid == stu.id:
                return stu
            
        return None
    
    def readMark(self, inputPath):
        with open(inputPath, "r") as f:
            lines = f.read().splitlines()
            
        for line in lines:
            if len(line.split("|")) != 4:
                continue
            
            cid, sid, mark, credits = line.split("|")
            
            if self.haveStuId(sid) == None or self.haveCourseId(cid) == None:
                continue
            
            course = self.haveCourseId(cid)
            stu = self.haveStuId(sid)

            course.addStu(sid)
            stu.addMark(Mark(cid, mark, credits))  
            
        return           
    
    def readDataFromFiles(self):
        self.readCourses("courses.txt")
        self.readStudents("students.txt")
        self.readMark("marks.txt")
    
        return
    
    def showCourse(self, course):
        if course == None:
            return 
        
        if len(course.students) == 0:
            print(f"- There aren't any students attend course {course.id}!")
            return 
        
        print(f'- {course}:')
        for sid in course.students:
            stu = self.haveStuId(sid)
            print(f"    + {stu}")
            
        print()
    
    def showAllCourses(self):
        for course in self.courses:
            self.showCourse(course)
            
        return
    
    def showInforStudent(self, student):
        if student == None:
            return 
        
        print(f"- {student} attend:")
        for cid in student.courses:
            course = self.haveCourseId(cid)
            print(f'    + {course}')
        
        print()
        
    def showAllStudentGPA(self):
        print(f"- List of Students:")
        
        self.students.sort(key=lambda stu: stu.getGPA(), reverse=True)
        
        for stu in self.students:
            gpa = math.floor(stu.getGPA() * 10) / 10
            print(f"+ Student {stu.name:<6} ({stu.id}, {stu.dob})  | GPA = {gpa:.1f}")
            
        print()
        
            
    def showAll(self):
        return
    
def help_screen(stdscr, system=None):
    stdscr.clear()
    stdscr.addstr(1, 2, "HELP", curses.A_BOLD)

    stdscr.addstr(3, 4, "UP / DOWN : move")
    stdscr.addstr(4, 4, "ENTER     : select")
    stdscr.addstr(5, 4, "Q         : quit")

    stdscr.refresh()
    
    while True:
        key = stdscr.getch()
        if key == 27:      # ESC
            return

def show_gpa_screen(stdscr, system):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    stdscr.addstr(1, 2, "LIST OF STUDENTS (GPA)", curses.A_BOLD)

    system.students.sort(key=lambda s: s.getGPA(), reverse=True)

    y = 4
    for stu in system.students:
        if y >= h - 1:
            break   # tránh overflow

        gpa = math.floor(stu.getGPA() * 10) / 10
        text = f"{stu.name:<6} | {stu.id} | {stu.dob} | GPA: {gpa:.1f}"

        stdscr.addstr(y, 4, text[:w-5])
        y += 1

    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == 27:  # ESC
            return


def show_courses_screen(stdscr, system):
    stdscr.clear()
    stdscr.addstr(1, 2, "LIST OF COURSES", curses.A_BOLD)

    y = 3
    for course in system.courses:
        stdscr.addstr(y, 4, f"{course.id} - {course.name}")
        y += 1

    stdscr.refresh()
    
    while True:
        key = stdscr.getch()
        if key == 27:      # ESC
            return

def init_curses(stdscr):
    # Cấu hình terminal
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()

    # Fix ESC delay
    curses.set_escdelay(25)

    # Màu sắc
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()

        # Color pairs
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # selected
        curses.init_pair(2, curses.COLOR_WHITE, -1)                  # normal
        curses.init_pair(3, curses.COLOR_CYAN, -1)                   # title
        curses.init_pair(4, curses.COLOR_YELLOW, -1)                 # status

def main(stdscr):
    init_curses(stdscr)
    system = System()
    
    
    menu = [
        ("Show courses", show_courses_screen),
        ("Show GPAs", show_gpa_screen),
        ("Help", help_screen),
        ("Exit", None)
    ]
    
    current = 0
    
    while True:
        def print_mid(y, text, attr=0):
            h, w = stdscr.getmaxyx()
            x = (w - len(text)) // 2
            stdscr.addstr(y, x, text, attr)
        
        stdscr.clear()
        
        title = "STUDENT MARK MANAGEMENT SYSTEM CLI"
        print_mid(1, title, curses.A_BOLD)
        
        for i, (label, _) in enumerate(menu):
            attr = curses.A_REVERSE if i == current else 0
            print_mid(5 + i, label, attr) 
                    
        stdscr.refresh()
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            current = (current - 1) % len(menu)
        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(menu)
        elif key in (10, 13):  # Enter
            if menu[current][1] is None:
                break
            menu[current][1](stdscr, system)
        elif key in (ord('q'), ord('Q')):
            break
            
        
if __name__ == "__main__":
    curses.wrapper(main)