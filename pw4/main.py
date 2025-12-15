import curses
import math

from domains.System import System

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

    students = sorted(system.students, key=lambda s: s.calc_gpa(), reverse=True)

    y = 4
    for stu in students:
        if y >= h - 1:
            break   # tránh overflow

        gpa = math.floor(stu.calc_gpa() * 10) / 10
        text = f"{stu.get_name():<6} | {stu.get_id()} | {stu.get_dob()} | GPA: {gpa:.1f}"

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