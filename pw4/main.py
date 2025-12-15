# main.py — run program using curses UI

from input import load_data
from output import show_ui
from domains.system import SystemManageMark


def main():
    # Load students, courses, marks from input.txt
    students, courses = load_data("input.txt")

    # Create system manager object
    system = SystemManageMark(students, courses)

    # Launch UI (curses)
    show_ui(system)


if __name__ == "__main__":
    main()
