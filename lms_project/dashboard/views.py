from django.shortcuts import render, redirect
from accounts.models import Student
from courses.models import Course
from enrollments.models import Enrollment
from assignments.models import Assignment, Submission


def dashboard(request):

    # 🔴 ADMIN CHECK (Django login)
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, "accounts/admin_dashboard.html")

    # 🔵 STUDENT CHECK (session)
    if "user_id" not in request.session:
        return redirect("student_login")

    user_id = request.session["user_id"]

    student = Student.objects.get(id=user_id)

    courses = Course.objects.all()

    enrolled = Enrollment.objects.filter(student_id=user_id)
    enrolled_ids = enrolled.values_list("course_id", flat=True)

    assignments = Assignment.objects.filter(course_id__in=enrolled_ids)

    submissions = Submission.objects.filter(student_id=user_id).select_related("assignment")
    submitted_ids = submissions.values_list("assignment_id", flat=True)

    return render(request, "accounts/dashboard.html", {
        "student": student,
        "courses": courses,
        "enrolled_ids": enrolled_ids,
        "assignments": assignments,
        "submitted_ids": submitted_ids,
        "submissions": submissions
    })