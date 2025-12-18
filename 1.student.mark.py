from datetime import datetime

students = []
courses = []
marks = []


def isStudentId(stu_id: str) -> bool:
    if not stu_id:
        return False
    
    if not stu_id.isalnum():
        return False
    
    if len(stu_id) < 5:
        return False
    
    return True


def isStudentName(name: str) -> bool:
    if not name.strip():
        return False
    
    return all(ch.isalpha() or ch.isspace() for ch in name)


def isStudentDob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%d/%m/%Y")
        return True
    
    except ValueError:
        return False
    
def isCourseId(course_id: str) -> bool:
    if not course_id:
        return False
    
    return course_id.isalnum()


def isCourseName(name: str) -> bool:
    return len(name.strip()) > 0

def inputStudentId(s: str = "  Id: ") -> str:
    stu_id = input(s)
    
    while not isStudentId(stu_id):
        stu_id = input("  Invalid Id, enter again: ")
        
    return stu_id


def inputStudentName(s: str = "  Name: ") -> str:
    name = input(s)
    
    while not isStudentName(name):
        name = input("  Invalid name, enter again: ")
        
    return name


def inputStudentDob(s: str = "  DoB (dd/mm/yyyy): ") -> str:
    dob = input(s)
    
    while not isStudentDob(dob):
        dob = input("  Invalid DoB, enter again (dd/mm/yyyy): ")
    
    return dob

def inputCourseId(s: str = "  Course Id: ") -> str:
    course_id = input(s)
    
    while not isCourseId(course_id):
        course_id = input("  Invalid Course Id, enter again: ")
        
    return course_id


def inputCourseName(s: str = "  Course Name: ") -> str:
    name = input(s)
    
    while not isCourseName(name):
        name = input("  Invalid Course Name, enter again: ")
        
    return name

def inputStudents():
    n = int(input("Give me number of students in your class: "))

    for i in range(n):
        print(f"\nPlease add information for student {i + 1}:")
        stu_id = inputStudentId()
        name = inputStudentName()
        dob = inputStudentDob()

        student = {
            "id": stu_id,
            "name": name,
            "dob": dob
        }

        students.append(student)
        
def inputCourses():
    n = int(input("Give me number of courses: "))

    for i in range(n):
        print(f"\nPlease add information for course {i + 1}:")
        course_id = inputCourseId()
        course_name = inputCourseName()

        course = {
            "id": course_id,
            "name": course_name
        }

        courses.append(course)

def showStudents():
    print("\n===== STUDENT LIST =====")
    
    for i, stu in enumerate(students, start=1):
        print(f"{i}. ID: {stu['id']}, Name: {stu['name']}, DoB: {stu['dob']}")

def showCourses():
    print("\n===== COURSE LIST =====")
    
    for i, course in enumerate(courses, start=1):
        print(f"{i}. ID: {course['id']}, Name: {course['name']}")

def findStudentId(students : list, sid : str) -> int:
    for i, stu in enumerate(students):
        if stu["id"] == sid:
            return i
        
    return -1

def findCourseId(courses : list, cid : str) -> int:
    for i, course in enumerate(courses):
        if course["id"] == cid:
            return i
        
    return -1
    
def inputMark():
    showCourses()

    cid = inputCourseId("\nPlease choose a course: ")

    while findCourseId(courses, cid) == -1:
        cid = inputCourseId("- Course not found, choose again: ")

    index = findCourseId(courses, cid)

    print(
        f"Add mark for students in course "
        f"{courses[index]['id']} ({courses[index]['name']})"
    )

    mark = {
        "courseId": cid,
        "marks": []
    }

    for stu in students:
        while True:
            try:
                m = float(input(f"  {stu['id']} : "))
                if 0 <= m <= 10:
                    break
                else:
                    print("  Mark must be between 0 and 10")
            except ValueError:
                print("  Invalid number, enter again")

        mark["marks"].append(m)

    marks.append(mark)
    
def showMarks():
    print("\n===== MARK LIST =====")

    for mark in marks:
        cid = mark["courseId"]
        cidx = findCourseId(courses, cid)

        if cidx == -1:
            print(f"\nCourse {cid} not found")
            continue

        print(f"\nCourse: {courses[cidx]['id']} - {courses[cidx]['name']}")
        print("-" * 40)

        for stu, m in zip(students, mark["marks"]):
            print(f"{stu['id']:12} | {stu['name']:<20} | {m:5.2f}")
        
if __name__ == "__main__":
    inputStudents()
    inputCourses()
    showStudents()
    
    inputMark()
    showMarks()
    
    