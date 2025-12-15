# input.py
from domains.Student import Student
from domains.Course import Course
from domains.Mark import Mark


def load_data(path):
    students = []
    courses = []

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    i = 0
    n_student = int(lines[i]); i += 1

    # --- LOAD STUDENTS ---
    for _ in range(n_student):
        sid = lines[i]; i += 1
        name = lines[i]; i += 1
        dob = lines[i]; i += 1
        s = Student(sid, name, dob)
        students.append(s)

    n_course = int(lines[i]); i += 1

    # --- LOAD COURSES + MARKS ---
    for _ in range(n_course):
        cid = lines[i]; i += 1
        cname = lines[i]; i += 1
        credit = int(lines[i]); i += 1
        c = Course(cid, cname)
        courses.append(c)

        for s in students:
            mark_value = float(lines[i]); i += 1
            mark = Mark(mark_value, credit, cid)
            s.add_mark(mark)

    return students, courses
