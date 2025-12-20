from datetime import datetime
import math, numpy as np 
import curses

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
                        students_path: str = "students.txt",
                        courses_path: str = "courses.txt",
                        marks_path: str = "mark.txt"):
        self.read_students_from_file(students_path)
        self.read_courses_from_file(courses_path)
        self.read_marks_from_file(marks_path)


class Input:
    def __init__(self, system: SystemManagementMark):
        self.system = system

    def input_all(self):
        self.system.inputStudents()
        self.system.inputCourses()
        self.system.inputMarks()

class CLI:
    def __init__(self):
        self.menu_items = [
            "Add new student",
            "Add new course",
            "Add marks for course",
            "View student list",
            "View course list",
            "View student's gpa",
            "Exit"
        ]
        
        # Loading inital data
        self.system = SystemManagementMark()
        self.system.load_from_files()
        
        self.MENU_WIDTH = 45
        self.selected_menu = 0
        self.active_menu = 0 
        
        # Fake data 
        self.students = []
        for i in range(30):
            self.students.append({"id": f"S{i+1:03d}", "name": f"Student {i+1}", "gpa": 3.0 + (i % 10) / 10})
            
        self.courses = []
        for i in range(20):
            self.courses.append({"id": f"CS{i+101}", "name": f"Course {i+1}"})
            
        # Real data
        self.students_gpa_data = self.system.get_students_sorted_by_gpa_data()
        self.courses_data = self.system.get_courses_data()
        self.students_data = self.system.get_students_data()
        
    
    def start(self):
        curses.wrapper(self.run)
    
    def init_CLI(self, stdscr):
        curses.curs_set(0)
        stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.set_escdelay(25)
        
        self.height, self.width = stdscr.getmaxyx()
        if self.height < 17 or self.width < 100:
            raise Exception("Terminal too small! Minimum size: 100x17")
        
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        
        self.menu_win = curses.newwin(self.height, self.MENU_WIDTH, 0, 0)
        self.content_win = curses.newwin(
            self.height, 
            self.width - self.MENU_WIDTH,
            0, 
            self.MENU_WIDTH
        )
        
        self.menu_win.keypad(True)
        self.content_win.keypad(True)
        
        pad_width = max(49, self.width - self.MENU_WIDTH - 4)
        self.students_data_pad = curses.newpad(max(1, len(self.students_data)) + 1, pad_width)
        self.courses_data_pad = curses.newpad(max(1, len(self.courses_data)) + 1, pad_width)
        self.students_gpa_data_pad = curses.newpad(max(1, len(self.students_gpa_data)) + 1, pad_width)

        self.student_scroll_pos = 0
        self.course_scroll_pos = 0
        self.gpa_scroll_pos = 0

        # Populate student pad
        for i, student in enumerate(self.students_data):
            # dob is a string like "dd/mm/yyyy"
            self.students_data_pad.addstr(
                i,
                0,
                f"{student['id']:<10} {student['name']:<25} {student['dob']:<12}",
            )

        # Populate course pad
        for i, course in enumerate(self.courses_data):
            self.courses_data_pad.addstr(i, 0, f"{course['id']:<12} {course['name']:<30}")

        # Populate GPA pad
        for i, student in enumerate(self.students_gpa_data):
            self.students_gpa_data_pad.addstr(
                i, 0, f"{student['id']:<10} {student['name']:<25} {student['gpa']:<10.2f}"
            )
        
    
    def draw_menu_win(self):
        self.menu_win.erase()
        self.menu_win.border()
        self.menu_win.bkgd(' ', curses.color_pair(2))
        self.menu_win.addstr(0, 2, " MENU ", curses.color_pair(4) | curses.A_BOLD)
        
        for i, item in enumerate(self.menu_items):
            if i == self.selected_menu:
                self.menu_win.attron(curses.color_pair(1) | curses.A_BOLD)
                self.menu_win.addstr(i + 2, 2, f"> {item}")
                self.menu_win.attroff(curses.color_pair(1) | curses.A_BOLD)
            else:
                self.menu_win.addstr(i + 2, 2, f"  {item}")
        
        # Add help text at bottom, accounting for border
        help_y = self.height - 3
        self.menu_win.addstr(help_y, 2, "Up/Down: Navigate", curses.color_pair(3))
        self.menu_win.addstr(help_y + 1, 2, "Enter: Open | ESC: Exit", curses.color_pair(3))
        
        self.menu_win.noutrefresh()
    
    def draw_content_win(self):
        self.content_win.erase()
        self.content_win.border()
        self.content_win.bkgd(' ', curses.color_pair(2))
        
        # Default welcome screen
        if self.active_menu == -1:
            self.content_win.addstr(0, 2, " WELCOME ", curses.color_pair(4) | curses.A_BOLD)
            
            # Welcome content
            center_y = self.height // 2 - 5
            center_x = (self.width - self.MENU_WIDTH) // 2
            
            welcome_text = [
                "╔═══════════════════════════════════╗",
                "║   STUDENT MANAGEMENT SYSTEM       ║",
                "╚═══════════════════════════════════╝",
                "",
                "Welcome to the Student Management CLI",
                "",
                "Features:",
                "• Add and manage students",
                "• Add and manage courses",
                "     • Track student marks and GPA",
                "   • View comprehensive reports",
                "",
                "  Select a menu item to begin!"
            ]
            
            for i, line in enumerate(welcome_text):
                x_pos = center_x - len(line) // 2
                if x_pos < 2:
                    x_pos = 2
                try:
                    if i < 3:  # Header
                        self.content_win.addstr(center_y + i, x_pos, line, curses.color_pair(4) | curses.A_BOLD)
                    elif "Features:" in line or "Getting Started:" in line:
                        self.content_win.addstr(center_y + i, x_pos, line, curses.color_pair(3) | curses.A_BOLD)
                    else:
                        self.content_win.addstr(center_y + i, x_pos, line)
                except:
                    pass  # Ignore if text doesn't fit
            
            self.content_win.noutrefresh()
            return
        
        # Regular menu content
        menu_option = self.menu_items[self.active_menu]
        self.content_win.addstr(0, 2, f" {menu_option.upper()} ", curses.color_pair(4) | curses.A_BOLD)
        
        # Display different content based on selected menu
        if self.active_menu == 0:  # Add new student
            self.content_win.addstr(2, 2, "Add New Student Form", curses.A_UNDERLINE)
            self.content_win.addstr(4, 2, "Student ID: _____________")
            self.content_win.addstr(5, 2, "Name:       _____________")
            self.content_win.addstr(6, 2, "GPA:        _____________")
            self.content_win.addstr(8, 2, "[Press Enter to submit]", curses.color_pair(3))
            self.content_win.addstr(10, 2, "Press Q to return to home", curses.color_pair(5))
        
        elif self.active_menu == 1:  # Add new course
            self.content_win.addstr(2, 2, "Add New Course Form", curses.A_UNDERLINE)
            self.content_win.addstr(4, 2, "Course ID:   _____________")
            self.content_win.addstr(5, 2, "Course Name: _____________")
            self.content_win.addstr(8, 2, "[Press Enter to submit]", curses.color_pair(3))
            self.content_win.addstr(10, 2, "Press Q to return to home", curses.color_pair(5))
        
        elif self.active_menu == 2:  # Add marks
            self.content_win.addstr(2, 2, "Add Marks for Course", curses.A_UNDERLINE)
            self.content_win.addstr(4, 2, "Student ID: _____________")
            self.content_win.addstr(5, 2, "Course ID:  _____________")
            self.content_win.addstr(6, 2, "Mark:       _____________")
            self.content_win.addstr(8, 2, "[Press Enter to submit]", curses.color_pair(3))
            self.content_win.addstr(10, 2, "Press Q to return to home", curses.color_pair(5))
        
        elif self.active_menu == 3:  # View student list
            self.content_win.addstr(2, 2, "Student List", curses.A_UNDERLINE)
            y = 4
            self.content_win.addstr(y, 2, f"{'ID':<10} {'Name':<25} {'DOB':<10}", curses.A_BOLD)
            y += 1
            self.content_win.addstr(y, 2, "-" * 45)
            
            help_y = self.height - 2
            self.content_win.addstr(help_y, 2, "W/S: Scroll | Q: Back to Home", curses.color_pair(5))
            
            total = len(self.students_data)
            visible = self.height - 8
            info = f"[{self.student_scroll_pos + 1}-{min(self.student_scroll_pos + visible, total)}/{total}]"
            self.content_win.addstr(2, self.width - self.MENU_WIDTH - len(info) - 4, info, curses.color_pair(3))
        
        elif self.active_menu == 4:  # View course list
            self.content_win.addstr(2, 2, "Course List", curses.A_UNDERLINE)
            y = 4
            self.content_win.addstr(y, 2, f"{'ID':<12} {'Course Name':<30}", curses.A_BOLD)
            y += 1
            self.content_win.addstr(y, 2, "-" * 42)
            
            help_y = self.height - 2
            self.content_win.addstr(help_y, 2, "W/S: Scroll | Q: Back to Home", curses.color_pair(5))
            
            # Show scroll position
            total = len(self.courses_data)
            visible = self.height - 8
            info = f"[{self.course_scroll_pos + 1}-{min(self.course_scroll_pos + visible, total)}/{total}]"
            self.content_win.addstr(2, self.width - self.MENU_WIDTH - len(info) - 4, info, curses.color_pair(3))
        
        elif self.active_menu == 5:  # View GPA
            self.content_win.addstr(2, 2, "Student's GPA List", curses.A_UNDERLINE)
            y = 4
            self.content_win.addstr(y, 2, f"{'ID':<10} {'Name':<25} {'GPA':<10}", curses.A_BOLD)
            y += 1
            self.content_win.addstr(y, 2, "-" * 45)
            
            help_y = self.height - 2
            self.content_win.addstr(help_y, 2, "W/S: Scroll | Q: Back to Home", curses.color_pair(5))
            
            total = len(self.students_gpa_data)
            visible = self.height - 8
            info = f"[{self.gpa_scroll_pos + 1}-{min(self.gpa_scroll_pos + visible, total)}/{total}]"
            self.content_win.addstr(2, self.width - self.MENU_WIDTH - len(info) - 4, info, curses.color_pair(3))
        
        elif self.active_menu == 6:  # Exit
            self.content_win.addstr(2, 2, "Exit Application", curses.A_UNDERLINE)
            self.content_win.addstr(4, 2, "Press Enter to exit", curses.color_pair(3))
            self.content_win.addstr(5, 2, "or ESC to cancel")
        
        self.content_win.noutrefresh()
    
    def refresh_student_pad(self):
        """Refresh student pad with current scroll position."""
        pad_top = self.student_scroll_pos
        screen_top = 7
        screen_bottom = self.height - 3
        screen_left = self.MENU_WIDTH + 2
        screen_right = self.width - 2

        self.students_data_pad.noutrefresh(
            pad_top, 0,
            screen_top, screen_left,
            screen_bottom, screen_right,
        )

    def refresh_course_pad(self):
        """Refresh course pad with current scroll position."""
        pad_top = self.course_scroll_pos
        screen_top = 7
        screen_bottom = self.height - 3
        screen_left = self.MENU_WIDTH + 2
        screen_right = self.width - 2

        self.courses_data_pad.noutrefresh(
            pad_top, 0,
            screen_top, screen_left,
            screen_bottom, screen_right,
        )

    def refresh_gpa_pad(self):
        """Refresh GPA pad with current scroll position."""
        pad_top = self.gpa_scroll_pos
        screen_top = 7
        screen_bottom = self.height - 3
        screen_left = self.MENU_WIDTH + 2
        screen_right = self.width - 2

        self.students_gpa_data_pad.noutrefresh(
            pad_top, 0,
            screen_top, screen_left,
            screen_bottom, screen_right,
        )
    
    def draw_init_CLI(self):
        self.draw_menu_win()
        self.draw_content_win()
        
        if self.active_menu == 3:
            self.refresh_student_pad()
        elif self.active_menu == 4:
            self.refresh_course_pad()
        elif self.active_menu == 5:
            self.refresh_gpa_pad()

        curses.doupdate()
    
    def run(self, stdscr):
        self.init_CLI(stdscr)
        self.draw_init_CLI()
        
        in_scroll_mode = False  
        
        while True:
            key = stdscr.getch()
            
            if key == 27:  # ESC key
                if in_scroll_mode:
                    in_scroll_mode = False
                    self.draw_init_CLI()
                else:
                    break
            
            elif self.active_menu == 3 and key in [ord('w'), ord('W'), ord('s'), ord('S'), ord('q'), ord('Q')]:
                visible_lines = self.height - 8

                if key in [ord('w'), ord('W')]:
                    in_scroll_mode = True
                    self.student_scroll_pos = max(0, self.student_scroll_pos - 1)
                    self.draw_init_CLI()
                elif key in [ord('s'), ord('S')]:
                    in_scroll_mode = True
                    max_scroll = max(0, len(self.students_data) - visible_lines)
                    self.student_scroll_pos = min(max_scroll, self.student_scroll_pos + 1)
                    self.draw_init_CLI()
                elif key in [ord('q'), ord('Q')]:
                    in_scroll_mode = False
                    self.active_menu = -1
                    self.draw_init_CLI()

            elif self.active_menu == 4 and key in [ord('w'), ord('W'), ord('s'), ord('S'), ord('q'), ord('Q')]:
                visible_lines = self.height - 8

                if key in [ord('w'), ord('W')]:
                    in_scroll_mode = True
                    self.course_scroll_pos = max(0, self.course_scroll_pos - 1)
                    self.draw_init_CLI()
                elif key in [ord('s'), ord('S')]:
                    in_scroll_mode = True
                    max_scroll = max(0, len(self.courses_data) - visible_lines)
                    self.course_scroll_pos = min(max_scroll, self.course_scroll_pos + 1)
                    self.draw_init_CLI()
                elif key in [ord('q'), ord('Q')]:
                    in_scroll_mode = False
                    self.active_menu = -1
                    self.draw_init_CLI()

            elif self.active_menu == 5 and key in [ord('w'), ord('W'), ord('s'), ord('S'), ord('q'), ord('Q')]:
                visible_lines = self.height - 8

                if key in [ord('w'), ord('W')]:
                    in_scroll_mode = True
                    self.gpa_scroll_pos = max(0, self.gpa_scroll_pos - 1)
                    self.draw_init_CLI()
                elif key in [ord('s'), ord('S')]:
                    in_scroll_mode = True
                    max_scroll = max(0, len(self.students_gpa_data) - visible_lines)
                    self.gpa_scroll_pos = min(max_scroll, self.gpa_scroll_pos + 1)
                    self.draw_init_CLI()
                elif key in [ord('q'), ord('Q')]:
                    in_scroll_mode = False
                    self.active_menu = -1
                    self.draw_init_CLI()

            elif self.active_menu in [0, 1, 2] and key in [ord('q'), ord('Q')]:
                # Quay về home screen
                self.active_menu = -1
                self.draw_init_CLI()
            
            elif not in_scroll_mode:
                if key == curses.KEY_UP:
                    self.selected_menu = max(0, self.selected_menu - 1)
                    self.draw_menu_win()
                    curses.doupdate()
                
                elif key == curses.KEY_DOWN:
                    self.selected_menu = min(len(self.menu_items) - 1, self.selected_menu + 1)
                    self.draw_menu_win()
                    curses.doupdate()
                
                elif key in (curses.KEY_ENTER, 10, 13):  # Enter key
                    if self.selected_menu == 6:  # Exit option
                        break
                    else:
                        self.active_menu = self.selected_menu
                        self.student_scroll_pos = 0
                        self.course_scroll_pos = 0
                        self.gpa_scroll_pos = 0

                        if self.active_menu in [3, 4, 5]:
                            in_scroll_mode = True
                        
                        self.draw_init_CLI()

if __name__ == "__main__":
    # After run python 3.student.mark.py, you should press Enter, q to use fully this CLI.
    # Now, three first function aren't avaleble.
    # The option is so boring!
    CLI().start()