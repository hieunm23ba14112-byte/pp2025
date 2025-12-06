import math
import numpy as np

class Mark:
    def __init__(self, cid, mark, credits):
        self.courseId = cid
        self.mark = float(mark)
        self.credits = int(credits)
        
    def __str__(self):
        return self.mark + " in course " + self.courseId
    
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
            totalMark += mark.mark
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
            cid, sid, mark, credits = line.split("|")
            
            if self.haveStuId(sid) == None or self.haveCourseId(cid) == None:
                continue
            
            course = self.haveCourseId(cid)
            stu = self.haveStuId(sid)

            course.addStu(sid)
            stu.addMark(Mark(cid, mark, credits))  
            
        return           
    
    def readInput(self):
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
    
    def showStudent(self, student):
        if student == None:
            return 
        
        print(f"- {student}")
        
    def showAllStudentGPA(self):
        print(f"- List of Students:")
        
        self.students.sort(key=lambda stu: stu.getGPA(), reverse=True)
        
        for stu in self.students:
            print(f"    + {stu} have GPA = {stu.getGPA()}")
        
            
    def showAll(self):
        return
             
if __name__ == "__main__":
    system = System()
    system.readInput()
    print()
    
    system.showAllStudentGPA()    
    


    
    