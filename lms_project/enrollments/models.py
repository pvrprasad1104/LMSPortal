from django.db import models
from accounts.models import Student
from courses.models import Course
from assignments.models import Submission
from quizzes.models import Result

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    progress = models.IntegerField(default=0)

    def update_progress(self):
        assignment_done = Submission.objects.filter(
            student=self.student,
            assignment__course=self.course
        ).count()

        quiz_done = Result.objects.filter(
            student=self.student,
            quiz__course=self.course
        ).count()

        progress = 10  # base

        progress += assignment_done * 30
        progress += quiz_done * 30

        if progress > 100:
            progress = 100

        self.progress = progress
        self.save()