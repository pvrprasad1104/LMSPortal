from django.db import models
from django.core.validators import FileExtensionValidator

class Student(models.Model):
    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.PositiveBigIntegerField()
    password = models.CharField(max_length=200)

    ROLE_CHOICES = (
        ("student", "Student"),
        ("admin", "Admin"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE)

    bio = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    pincode = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    profile_pic = models.ImageField(upload_to="studentdp/", null=True)

    resume = models.FileField(
        upload_to="resume/",
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])]
    )

    def __str__(self):
        return self.user.name
class AdminUser(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username
