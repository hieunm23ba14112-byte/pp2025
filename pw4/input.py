from domains.SystemManagementMark import SystemManagementMark

class Input:
    def __init__(self, system: SystemManagementMark):
        self.system = system

    def input_all(self):
        self.system.inputStudents()
        self.system.inputCourses()
        self.system.inputMarks()