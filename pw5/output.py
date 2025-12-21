from domains.SystemManagementMark import SystemManagementMark
import curses

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
        # Be permissive: different terminals/environments may start smaller.
        # The UI will still work; it may just show fewer rows/columns.
        if self.height < 10 or self.width < 50:
            raise Exception(f"Terminal too small! Minimum size: 50x10 (got {self.width}x{self.height})")
        
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