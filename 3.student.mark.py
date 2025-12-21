from datetime import datetime
import math, numpy as np 
import curses
import curses.textpad

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

    def add_student(self, sid, name, dob):
        """Add a new student to the system"""
        self.__students.append(Student(sid, name, dob))
        
    def add_course(self, cid, name):
        """Add a new course to the system"""
        self.__courses.append(Course(cid, name))
        
    def add_mark_for_student(self, sid, cid, mark_value, credit=3):
        """Add a mark for a student in a specific course"""
        # Find or create Mark object for the course
        mark_obj = None
        for m in self.__marks:
            if m.get_course_id() == cid:
                mark_obj = m
                break
        
        if mark_obj is None:
            mark_obj = Mark(cid)
            self.__marks.append(mark_obj)
        
        mark_obj.add_mark(sid, mark_value)
        mark_obj.add_credit(sid, credit)

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

    def read_students_from_file(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]

            n = int(lines[0])
            idx = 1
            for _ in range(n):
                sid = lines[idx]; idx += 1
                name = lines[idx]; idx += 1
                dob = lines[idx]; idx += 1
                self.__students.append(Student(sid, name, dob))
        except FileNotFoundError:
            pass

    def read_courses_from_file(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]

            n = int(lines[0])
            idx = 1
            for _ in range(n):
                cid = lines[idx]; idx += 1
                name = lines[idx]; idx += 1
                self.__courses.append(Course(cid, name))
        except FileNotFoundError:
            pass

    def read_marks_from_file(self, path: str, default_credit: int = 1):
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]

            current_mark_obj = None
            for line in lines:
                parts = line.split()
                if len(parts) == 1:
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
        except FileNotFoundError:
            pass

    def load_from_files(self,
                        students_path: str = "./input_data/students.txt",
                        courses_path: str = "./input_data/courses.txt",
                        marks_path: str = "./input_data/mark.txt"):
        self.read_students_from_file(students_path)
        self.read_courses_from_file(courses_path)
        self.read_marks_from_file(marks_path)


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
        
        # Loading initial data
        self.system = SystemManagementMark()
        self.system.load_from_files()
        
        self.MENU_WIDTH = 45
        self.selected_menu = 0
        self.active_menu = -1
        
        # Real data
        self.update_data()
        
    def update_data(self):
        """Update all data from system"""
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
        if self.height < 30 or self.width < 110:
            raise Exception("Terminal too small! Minimum size: 100x17")
        
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
        
        self.menu_win = curses.newwin(self.height, self.MENU_WIDTH, 0, 0)
        self.content_win = curses.newwin(
            self.height, 
            self.width - self.MENU_WIDTH,
            0, 
            self.MENU_WIDTH
        )
        
        self.menu_win.keypad(True)
        self.content_win.keypad(True)
        
        self.recreate_pads()

        self.student_scroll_pos = 0
        self.course_scroll_pos = 0
        self.gpa_scroll_pos = 0
        
    def recreate_pads(self):
        """Recreate pads with updated data"""
        pad_width = max(49, self.width - self.MENU_WIDTH - 4)
        self.students_data_pad = curses.newpad(max(1, len(self.students_data)) + 1, pad_width)
        self.courses_data_pad = curses.newpad(max(1, len(self.courses_data)) + 1, pad_width)
        self.students_gpa_data_pad = curses.newpad(max(1, len(self.students_gpa_data)) + 1, pad_width)

        # Populate student pad
        for i, student in enumerate(self.students_data):
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
                "Select a menu item to begin!"
            ]
            
            for i, line in enumerate(welcome_text):
                x_pos = center_x - len(line) // 2
                if x_pos < 2:
                    x_pos = 2
                try:
                    if i < 3:
                        self.content_win.addstr(center_y + i, x_pos, line, curses.color_pair(4) | curses.A_BOLD)
                    elif "Features:" in line:
                        self.content_win.addstr(center_y + i, x_pos, line, curses.color_pair(3) | curses.A_BOLD)
                    else:
                        self.content_win.addstr(center_y + i, x_pos, line)
                except:
                    pass
            
            self.content_win.noutrefresh()
            return
        
        # Regular menu content
        menu_option = self.menu_items[self.active_menu]
        self.content_win.addstr(0, 2, f" {menu_option.upper()} ", curses.color_pair(4) | curses.A_BOLD)
        
        if self.active_menu == 0:  # Add new student
            self.content_win.addstr(2, 2, "Add New Student Form", curses.A_UNDERLINE)
            self.content_win.addstr(4, 2, "Fill in the form below and press Enter")
            self.content_win.addstr(6, 2, "Press Enter to start", curses.color_pair(3))
            self.content_win.addstr(8, 2, "Press Q to return to home", curses.color_pair(5))
        
        elif self.active_menu == 1:  # Add new course
            self.content_win.addstr(2, 2, "Add New Course Form", curses.A_UNDERLINE)
            self.content_win.addstr(4, 2, "Fill in the form below and press Enter")
            self.content_win.addstr(6, 2, "Press Enter to start", curses.color_pair(3))
            self.content_win.addstr(8, 2, "Press Q to return to home", curses.color_pair(5))
        
        elif self.active_menu == 2:  # Add marks
            self.content_win.addstr(2, 2, "Add Marks for Course", curses.A_UNDERLINE)
            self.content_win.addstr(4, 2, "Fill in the form below and press Enter")
            self.content_win.addstr(6, 2, "Press Enter to start", curses.color_pair(3))
            self.content_win.addstr(8, 2, "Press Q to return to home", curses.color_pair(5))
        
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
    
    def show_add_student_form(self, stdscr):
        """Interactive form to add a new student"""
        form_height = 19
        form_width = 60
        start_y = (self.height - form_height) // 2
        start_x = self.MENU_WIDTH + (self.width - self.MENU_WIDTH - form_width) // 2
        
        form_win = curses.newwin(form_height, form_width, start_y, start_x)
        form_win.keypad(True)
        
        fields = {
            'id': '',
            'name': '',
            'dob': ''
        }
        
        current_field = 0
        field_names = ['id', 'name', 'dob']
        error_msg = ''
        
        while True:
            form_win.erase()
            form_win.border()
            form_win.bkgd(' ', curses.color_pair(2))
            form_win.addstr(0, 2, " ADD NEW STUDENT ", curses.color_pair(4) | curses.A_BOLD)
            
            # Draw fields
            y = 2
            for i, fname in enumerate(field_names):
                label = f"Student ID:" if fname == 'id' else f"Name:" if fname == 'name' else "DoB (dd/mm/yyyy):"
                form_win.addstr(y, 2, label, curses.A_BOLD if i == current_field else 0)
                
                # Draw input box
                box_y = y + 1
                box_text = fields[fname] + '_' if i == current_field else fields[fname]
                box_text = box_text[:40]  # Limit display length
                
                form_win.addstr(box_y, 2, "┌" + "─" * 52 + "┐")
                form_win.addstr(box_y + 1, 2, "│ " + box_text.ljust(51) + "│")
                form_win.addstr(box_y + 2, 2, "└" + "─" * 52 + "┘")
                
                y += 5
            
            # Show error message
            if error_msg:
                form_win.addstr(16, 2, error_msg[:55], curses.color_pair(6) | curses.A_BOLD)
            
            # Show instructions
            form_win.addstr(form_height - 2, 2, "Tab: Next | Enter: Submit | ESC: Cancel", curses.color_pair(5))
            
            form_win.refresh()
            
            key = form_win.getch()
            
            if key == 27:  # ESC
                return False
            elif key == 9:  # Tab
                current_field = (current_field + 1) % 3
                error_msg = ''
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                # Validate
                sid = fields['id'].strip()
                name = fields['name'].strip()
                dob = fields['dob'].strip()
                
                if not self.system.isStudentId(sid):
                    error_msg = "Invalid ID! (min 5 alphanumeric chars)"
                    current_field = 0
                elif not self.system.isStudentName(name):
                    error_msg = "Invalid Name! (letters and spaces only)"
                    current_field = 1
                elif not self.system.isStudentDob(dob):
                    error_msg = "Invalid DoB! (use dd/mm/yyyy format)"
                    current_field = 2
                else:
                    # Add student
                    self.system.add_student(sid, name, dob)
                    self.system.write_students_to_file()
                    self.update_data()
                    self.recreate_pads()
                    
                    # Show success message
                    form_win.erase()
                    form_win.border()
                    form_win.bkgd(' ', curses.color_pair(3))
                    form_win.addstr(form_height // 2 - 1, form_width // 2 - 10, "✓ STUDENT ADDED!", curses.color_pair(3) | curses.A_BOLD)
                    form_win.addstr(form_height // 2 + 1, form_width // 2 - 12, "Press any key to continue")
                    form_win.refresh()
                    form_win.getch()
                    return True
            elif key == curses.KEY_BACKSPACE or key == 127:
                fname = field_names[current_field]
                if fields[fname]:
                    fields[fname] = fields[fname][:-1]
                    error_msg = ''
            elif 32 <= key <= 126:  # Printable characters
                fname = field_names[current_field]
                if len(fields[fname]) < 40:
                    fields[fname] += chr(key)
                    error_msg = ''
    
    def show_add_course_form(self, stdscr):
        """Interactive form to add a new course"""
        form_height = 13
        form_width = 60
        start_y = (self.height - form_height) // 2
        start_x = self.MENU_WIDTH + (self.width - self.MENU_WIDTH - form_width) // 2
        
        form_win = curses.newwin(form_height, form_width, start_y, start_x)
        form_win.keypad(True)
        
        fields = {
            'id': '',
            'name': ''
        }
        
        current_field = 0
        field_names = ['id', 'name']
        error_msg = ''
        
        while True:
            form_win.erase()
            form_win.border()
            form_win.bkgd(' ', curses.color_pair(2))
            form_win.addstr(0, 2, " ADD NEW COURSE ", curses.color_pair(4) | curses.A_BOLD)
            
            # Draw fields
            y = 2
            for i, fname in enumerate(field_names):
                label = f"Course ID:" if fname == 'id' else "Course Name:"
                form_win.addstr(y, 2, label, curses.A_BOLD if i == current_field else 0)
                
                # Draw input box
                box_y = y + 1
                box_text = fields[fname] + '_' if i == current_field else fields[fname]
                box_text = box_text[:40]
                
                form_win.addstr(box_y, 2, "┌" + "─" * 52 + "┐")
                form_win.addstr(box_y + 1, 2, "│ " + box_text.ljust(51) + "│")
                form_win.addstr(box_y + 2, 2, "└" + "─" * 52 + "┘")
                
                y += 4
            
            # Show error message
            if error_msg:
                form_win.addstr(10, 2, error_msg[:55], curses.color_pair(6) | curses.A_BOLD)
            
            # Show instructions
            form_win.addstr(form_height - 2, 2, "Tab: Next | Enter: Submit | ESC: Cancel", curses.color_pair(5))
            
            form_win.refresh()
            
            key = form_win.getch()
            
            if key == 27:  # ESC
                return False
            elif key == 9:  # Tab
                current_field = (current_field + 1) % 2
                error_msg = ''
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                # Validate
                cid = fields['id'].strip()
                name = fields['name'].strip()
                
                if not self.system.isCourseId(cid):
                    error_msg = "Invalid Course ID! (alphanumeric only)"
                    current_field = 0
                elif not self.system.isCourseName(name):
                    error_msg = "Invalid Course Name! (cannot be empty)"
                    current_field = 1
                else:
                    # Add course
                    self.system.add_course(cid, name)
                    self.system.write_courses_to_file()
                    self.update_data()
                    self.recreate_pads()
                    
                    # Show success message
                    form_win.erase()
                    form_win.border()
                    form_win.bkgd(' ', curses.color_pair(3))
                    form_win.addstr(form_height // 2 - 1, form_width // 2 - 10, "✓ COURSE ADDED!", curses.color_pair(3) | curses.A_BOLD)
                    form_win.addstr(form_height // 2 + 1, form_width // 2 - 12, "Press any key to continue")
                    form_win.refresh()
                    form_win.getch()
                    return True
            elif key == curses.KEY_BACKSPACE or key == 127:
                fname = field_names[current_field]
                if fields[fname]:
                    fields[fname] = fields[fname][:-1]
                    error_msg = ''
            elif 32 <= key <= 126:
                fname = field_names[current_field]
                if len(fields[fname]) < 40:
                    fields[fname] += chr(key)
                    error_msg = ''
    
    def show_add_mark_form(self, stdscr):
        """Interactive form to add marks for a student"""
        form_height = 21
        form_width = 60
        start_y = (self.height - form_height) // 2
        start_x = self.MENU_WIDTH + (self.width - self.MENU_WIDTH - form_width) // 2
        
        form_win = curses.newwin(form_height, form_width, start_y, start_x)
        form_win.keypad(True)
        
        fields = {
            'student_id': '',
            'course_id': '',
            'mark': '',
            'credit': '3'
        }
        
        current_field = 0
        field_names = ['student_id', 'course_id', 'mark', 'credit']
        error_msg = ''
        
        while True:
            form_win.erase()
            form_win.border()
            form_win.bkgd(' ', curses.color_pair(2))
            form_win.addstr(0, 2, " ADD MARK ", curses.color_pair(4) | curses.A_BOLD)
            
            # Draw fields
            y = 2
            for i, fname in enumerate(field_names):
                if fname == 'student_id':
                    label = "Student ID:"
                elif fname == 'course_id':
                    label = "Course ID:"
                elif fname == 'mark':
                    label = "Mark (0-10):"
                else:
                    label = "Credit:"
                
                form_win.addstr(y, 2, label, curses.A_BOLD if i == current_field else 0)
                
                # Draw input box
                box_y = y + 1
                box_text = fields[fname] + '_' if i == current_field else fields[fname]
                box_text = box_text[:40]
                
                form_win.addstr(box_y, 2, "┌" + "─" * 52 + "┐")
                form_win.addstr(box_y + 1, 2, "│ " + box_text.ljust(51) + "│")
                form_win.addstr(box_y + 2, 2, "└" + "─" * 52 + "┘")
                
                y += 4
            
            # Show error message
            if error_msg:
                form_win.addstr(18, 2, error_msg[:55], curses.color_pair(6) | curses.A_BOLD)
            
            # Show instructions
            form_win.addstr(form_height - 2, 2, "Tab: Next | Enter: Submit | ESC: Cancel", curses.color_pair(5))
            
            form_win.refresh()
            
            key = form_win.getch()
            
            if key == 27:  # ESC
                return False
            elif key == 9:  # Tab
                current_field = (current_field + 1) % 4
                error_msg = ''
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                # Validate
                sid = fields['student_id'].strip()
                cid = fields['course_id'].strip()
                mark_str = fields['mark'].strip()
                credit_str = fields['credit'].strip()
                
                # Check if student exists
                student_exists = any(s.get_id() == sid for s in self.system.get_students())
                if not student_exists:
                    error_msg = "Student ID not found!"
                    current_field = 0
                    continue
                
                # Check if course exists
                course_exists = any(c.get_id() == cid for c in self.system.get_courses())
                if not course_exists:
                    error_msg = "Course ID not found!"
                    current_field = 1
                    continue
                
                # Validate mark
                try:
                    mark_val = float(mark_str)
                    if mark_val < 0 or mark_val > 10:
                        error_msg = "Mark must be between 0 and 10!"
                        current_field = 2
                        continue
                except ValueError:
                    error_msg = "Invalid mark value!"
                    current_field = 2
                    continue
                
                # Validate credit
                try:
                    credit_val = int(credit_str)
                    if credit_val <= 0:
                        error_msg = "Credit must be positive!"
                        current_field = 3
                        continue
                except ValueError:
                    error_msg = "Invalid credit value!"
                    current_field = 3
                    continue
                
                # Add mark
                self.system.add_mark_for_student(sid, cid, mark_val, credit_val)
                self.system.write_marks_to_file()
                self.update_data()
                self.recreate_pads()
                
                # Show success message
                form_win.erase()
                form_win.border()
                form_win.bkgd(' ', curses.color_pair(3))
                form_win.addstr(form_height // 2 - 1, form_width // 2 - 8, "✓ MARK ADDED!", curses.color_pair(3) | curses.A_BOLD)
                form_win.addstr(form_height // 2 + 1, form_width // 2 - 12, "Press any key to continue")
                form_win.refresh()
                form_win.getch()
                return True
                
            elif key == curses.KEY_BACKSPACE or key == 127:
                fname = field_names[current_field]
                if fields[fname]:
                    fields[fname] = fields[fname][:-1]
                    error_msg = ''
            elif 32 <= key <= 126:
                fname = field_names[current_field]
                char = chr(key)
                
                # Only allow numbers and decimal point for mark
                if fname == 'mark' and char not in '0123456789.':
                    continue
                # Only allow numbers for credit
                if fname == 'credit' and char not in '0123456789':
                    continue
                
                if len(fields[fname]) < 40:
                    fields[fname] += char
                    error_msg = ''
    
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

            elif self.active_menu == 0 and key in (curses.KEY_ENTER, 10, 13):
                # Show add student form
                self.show_add_student_form(stdscr)
                self.active_menu = -1
                self.draw_init_CLI()

            elif self.active_menu == 1 and key in (curses.KEY_ENTER, 10, 13):
                # Show add course form
                self.show_add_course_form(stdscr)
                self.active_menu = -1
                self.draw_init_CLI()

            elif self.active_menu == 2 and key in (curses.KEY_ENTER, 10, 13):
                # Show add mark form
                self.show_add_mark_form(stdscr)
                self.active_menu = -1
                self.draw_init_CLI()

            elif self.active_menu in [0, 1, 2] and key in [ord('q'), ord('Q')]:
                # Return to home screen
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
    CLI().start()