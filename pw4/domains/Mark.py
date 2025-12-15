import math

class Mark:
    def __init__(self, mark, credits, courseId):
        self.mark = math.floor(mark * 10) / 10
        self.credits = credits
        self.courseId = courseId

    def get_mark(self):
        return self.mark

    def get_credits(self):
        return self.credits

    def get_course_id(self):
        return self.courseId

    def __str__(self):
        return f"(Course: {self.courseId}, Mark: {self.mark}, Credits: {self.credits})"
