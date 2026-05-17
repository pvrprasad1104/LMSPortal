from django.db import models
from accounts.models import Student


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=100)

    instructor_name = models.CharField(max_length=200)
    instructor_id = models.IntegerField(null=True,blank=True)   # NEW (important)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title