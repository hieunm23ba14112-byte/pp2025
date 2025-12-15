class Student:
    def __init__(self, sid, name, dob):
        self.id = sid
        self.name = name
        self.DoB = dob
        self.marks = []
        self.courses = []

    def add_mark(self, mark_obj):
        self.marks.append(mark_obj)
        self.courses.append(mark_obj.courseId)

    def calc_gpa(self):
        if not self.marks:
            return 0.0
        total = sum(m.mark * m.credits for m in self.marks)
        credits = sum(m.credits for m in self.marks)
        return round(total / credits, 2) if credits > 0 else 0.0

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_dob(self):
        return self.DoB

    def get_marks(self):
        return self.marks

    def __str__(self):
        marks_str = ", ".join(str(m) for m in self.marks)
        return f"Student[{self.id}, {self.name}, {self.DoB}] GPA={self.calc_gpa()} | Marks: {marks_str}"
