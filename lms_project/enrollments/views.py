from django.shortcuts import redirect, get_object_or_404
from .models import Enrollment
from courses.models import Course
from accounts.models import Student


def enroll_course(request, course_id):

    if 'user_id' not in request.session:
        return redirect('student_login')

    student = Student.objects.get(id=request.session['user_id'])

    course = get_object_or_404(Course, id=course_id)

    Enrollment.objects.get_or_create(
        student=student,
        course=course
    )

    return redirect('dashboard')


def unenroll_course(request, course_id):

    if "user_id" not in request.session:
        return redirect("student_login")

    student = Student.objects.get(id=request.session["user_id"])
    course = Course.objects.get(id=course_id)

    Enrollment.objects.filter(
        student=student,
        course=course
    ).delete()

    return redirect("dashboard")