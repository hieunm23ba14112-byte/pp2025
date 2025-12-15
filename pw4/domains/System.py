import math
import os

from .Student import Student
from .Course import Course
from .Mark import Mark


class System:
    """
    Quản lý danh sách Student / Course và mark, đọc từ thư mục input_data.
    Dùng API mới của Student / Course / Mark (calc_gpa, add_mark, add_student, ...).
    """

    def __init__(self, name: str = "Dark"):
        self.name = name
        self.students: list[Student] = []
        self.courses: list[Course] = []
        self._load_from_files()

    # --------- Helper paths ----------
    def _data_path(self, filename: str) -> str:
        """
        Trả về đường dẫn tuyệt đối tới file trong input_data,
        độc lập với thư mục làm việc hiện tại.
        """
        base_dir = os.path.dirname(os.path.dirname(__file__))  # .../pw4
        return os.path.join(base_dir, "input_data", filename)

    # --------- Load data ----------
    def _read_courses(self, filename: str = "courses.txt") -> None:
        path = self._data_path(filename)
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        for line in lines:
            cid, name = line.split("|")
            self.courses.append(Course(cid, name))

    def _read_students(self, filename: str = "students.txt") -> None:
        path = self._data_path(filename)
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        for line in lines:
            sid, name, dob = line.split("|")
            self.students.append(Student(sid, name, dob))

    def _find_course(self, cid: str) -> Course | None:
        for c in self.courses:
            if c.get_id() == cid:
                return c
        return None

    def _find_student(self, sid: str) -> Student | None:
        for s in self.students:
            if s.get_id() == sid:
                return s
        return None

    def _read_marks(self, filename: str = "marks.txt") -> None:
        path = self._data_path(filename)
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        for line in lines:
            parts = line.split("|")
            if len(parts) != 4:
                continue

            cid, sid, mark_str, credit_str = parts
            stu = self._find_student(sid)
            course = self._find_course(cid)
            if stu is None or course is None:
                continue

            try:
                mark_val = float(mark_str)
                credits = int(credit_str)
            except ValueError:
                continue

            m = Mark(mark_val, credits, cid)
            stu.add_mark(m)
            course.add_student(stu)

    def _load_from_files(self) -> None:
        self._read_courses()
        self._read_students()
        self._read_marks()

    # --------- Simple query helpers used by UI ----------
    def list_students_by_gpa_desc(self) -> list[Student]:
        return sorted(self.students, key=lambda s: s.calc_gpa(), reverse=True)

    def list_courses(self) -> list[Course]:
        return list(self.courses)
