from django.db import models
from courses.models import Course
from accounts.models import Student


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignments/')
    marks = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.assignment.title}"