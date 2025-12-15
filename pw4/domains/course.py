class Course:
    def __init__(self, cid, name):
        self.id = cid
        self.name = name
        self.studentList = []

    def add_student(self, student):
        if student not in self.studentList:
            self.studentList.append(student)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def __str__(self):
        return f"Course[{self.id}] {self.name} ({len(self.studentList)} students)"
