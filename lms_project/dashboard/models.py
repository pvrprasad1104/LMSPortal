from django.db import models
from accounts.models import Student

class Dashboard(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE)
    last_login_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name