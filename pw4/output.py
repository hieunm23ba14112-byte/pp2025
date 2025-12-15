import curses
import time
import textwrap


# ==================================================
# Helper: draw bordered window
# ==================================================
def draw_box(win, title=None):
    h, w = win.getmaxyx()
    win.box()

    if title:
        win.attron(curses.color_pair(3))
        win.addstr(0, 2, f" {title} ")
        win.attroff(curses.color_pair(3))


# ==================================================
# Sidebar menu
# ==================================================
def draw_sidebar(stdscr, menu, selected):
    h, w = stdscr.getmaxyx()
    side_w = 26

    sidebar = stdscr.subwin(h, side_w, 0, 0)
    sidebar.box()

    sidebar.attron(curses.color_pair(4))
    sidebar.addstr(1, 3, "MAIN MENU")
    sidebar.attroff(curses.color_pair(4))

    for i, item in enumerate(menu):
        y = 3 + i
        if i == selected:
            sidebar.attron(curses.color_pair(2) | curses.A_BOLD)
            sidebar.addstr(y, 2, f"> {item}")
            sidebar.attroff(curses.color_pair(2) | curses.A_BOLD)
        else:
            sidebar.addstr(y, 2, f"  {item}")


# ==================================================
# Status bar
# ==================================================
def draw_status(stdscr, msg):
    h, w = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(5))
    stdscr.addstr(h - 1, 1, msg.ljust(w - 2))
    stdscr.attroff(curses.color_pair(5))


# ==================================================
# Scrollable content window
# ==================================================
def scroll_window(stdscr, title, lines):
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    win = stdscr.subwin(h, w - 26, 0, 26)

    pos = 0
    while True:
        win.clear()
        draw_box(win, title)

        max_lines = h - 4
        page = lines[pos:pos + max_lines]

        y = 2
        for line in page:
            for seg in textwrap.wrap(line, w - 30):
                win.addstr(y, 2, seg)
                y += 1

        win.refresh()
        draw_status(stdscr, "↑↓ scroll • ENTER select • Q back")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP: pos = max(0, pos - 1)
        if key == curses.KEY_DOWN: pos = min(len(lines) - 1, pos + 1)
        if key in (ord("q"), ord("Q")): return None
        if key in (10, 13): return pos


# ==================================================
# Student detail
# ==================================================
def show_student(stdscr, stu):
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    win = stdscr.subwin(h, w - 26, 0, 26)

    while True:
        win.clear()
        draw_box(win, f"Student: {stu.get_name()}")

        lines = [
            f"ID     : {stu.get_id()}",
            f"Name   : {stu.get_name()}",
            f"DOB    : {stu.get_dob()}",
            f"GPA    : {stu.calc_gpa()}",
            "",
            "Marks:"
        ]

        for m in stu.get_marks():
            lines.append(f"- {m.get_course_id()}: {m.get_mark()} ({m.get_credits()}cr)")

        y = 2
        for line in lines:
            win.addstr(y, 2, line)
            y += 1

        draw_status(stdscr, "Q to go back")
        stdscr.refresh()
        win.refresh()

        key = stdscr.getch()
        if key in (ord("q"), ord("Q"), 10, 13):
            return


# ==================================================
# Dashboard
# ==================================================
def dashboard(stdscr, system):
    h, w = stdscr.getmaxyx()
    win = stdscr.subwin(h, w - 26, 0, 26)

    # Animation on open
    for i in range(1, 15):
        win.clear()
        draw_box(win, "Dashboard")

        win.attron(curses.color_pair(6))
        win.addstr(3, 5, f"Loading system... {i*7}%")
        win.attroff(curses.color_pair(6))

        win.refresh()
        time.sleep(0.02)

    win.clear()
    draw_box(win, "Dashboard")

    total_s = len(system.students)
    total_c = len(system.courses)

    avg_gpa = 0
    if total_s:
        avg_gpa = round(sum(s.calc_gpa() for s in system.students) / total_s, 2)

    stats = [
        f"Total Students : {total_s}",
        f"Total Courses  : {total_c}",
        f"Average GPA    : {avg_gpa}",
        "",
        "Top Students (GPA):"
    ]

    sorted_students = sorted(system.students, key=lambda s: s.calc_gpa(), reverse=True)
    for s in sorted_students[:5]:
        stats.append(f"- {s.get_name()} | {s.calc_gpa()}")

    y = 2
    for line in stats:
        win.addstr(y, 3, line)
        y += 1

    win.refresh()
    draw_status(stdscr, "UI Level 2 Active")


# ==================================================
# Main UI
# ==================================================
def show_ui(system):

    def ui(stdscr):
        curses.start_color()
        curses.use_default_colors()

        # color pairs
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, curses.COLOR_CYAN, -1)
        curses.init_pair(4, curses.COLOR_MAGENTA, -1)
        curses.init_pair(5, curses.COLOR_BLUE, -1)
        curses.init_pair(6, curses.COLOR_GREEN, -1)

        curses.curs_set(0)
        stdscr.clear()

        menu = ["Dashboard", "Students", "Courses", "Exit"]
        selected = 0

        while True:
            stdscr.clear()

            # LEFT SIDEBAR
            draw_sidebar(stdscr, menu, selected)

            # CONTENT AREA
            if selected == 0:
                dashboard(stdscr, system)

            elif selected == 1:
                stud_list = [f"{s.get_id()} - {s.get_name()} (GPA {s.calc_gpa()})"
                             for s in system.students]
                idx = scroll_window(stdscr, "Students", stud_list)
                if idx is not None:
                    show_student(stdscr, system.students[idx])

            elif selected == 2:
                course_lines = [f"{c.get_id()} - {c.get_name()}" for c in system.courses]
                scroll_window(stdscr, "Courses", course_lines)

            elif selected == 3:
                break

            draw_status(stdscr, "↑↓ navigate • ENTER select • Q quit")
            stdscr.refresh()

            key = stdscr.getch()
            if key == curses.KEY_UP:
                selected = (selected - 1) % len(menu)
            elif key == curses.KEY_DOWN:
                selected = (selected + 1) % len(menu)
            elif key in (ord("q"), ord("Q")):
                break
            elif key in (10, 13):  # Enter: handled automatically
                pass

    curses.wrapper(ui)
