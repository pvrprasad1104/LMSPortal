from django.shortcuts import render, redirect
from .models import Assignment, Submission
from enrollments.models import Enrollment
from accounts.models import Student

def submit_assignment(request, assignment_id):
    if "user_id" not in request.session:
        return redirect("student_login")

    if request.method == "POST":
        submission = Submission.objects.create(
            student_id=request.session["user_id"],
            assignment_id=assignment_id,
            file=request.FILES.get("file")
        )

        # 🔥 UPDATE PROGRESS
        assignment = Assignment.objects.get(id=assignment_id)

        enrollment = Enrollment.objects.filter(
            student_id=request.session["user_id"],
            course=assignment.course
        ).first()

        if enrollment:
            enrollment.progress += 20   # each assignment = 20%
            if enrollment.progress > 100:
                enrollment.progress = 100
            enrollment.save()

        return redirect("dashboard")

    assignment = Assignment.objects.get(id=assignment_id)

    return render(request, "assignments/submit.html", {
        "assignment": assignment
    })


def view_submissions(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")

    submissions = Submission.objects.all()

    return render(request, "assignments/submissions.html", {
        "submissions": submissions
    })


def give_marks(request, submission_id):
    if "admin_id" not in request.session:
        return redirect("admin_login")

    submission = Submission.objects.get(id=submission_id)

    if request.method == "POST":
        submission.marks = request.POST.get("marks")
        submission.save()
        return redirect("view_submissions")

    return render(request, "assignments/give_marks.html", {
        "submission": submission
    })


def create_assignment(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")

    from courses.models import Course
    courses = Course.objects.all()

    if request.method == "POST":
        Assignment.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            course_id=request.POST.get("course"),
            deadline=request.POST.get("deadline")
        )
        return redirect("admin_dashboard")

    return render(request, "assignments/create_assignment.html", {
        "courses": courses
    })
def assignments(request):
    if "user_id" not in request.session:
        return redirect("student_login")

    student = Student.objects.get(id=request.session["user_id"])

    enrollments = Enrollment.objects.filter(student=student)
    course_ids = enrollments.values_list("course_id", flat=True)

    assignments = Assignment.objects.filter(course_id__in=course_ids)

    submitted_ids = Submission.objects.filter(
        student=student
    ).values_list("assignment_id", flat=True)

    return render(request, "assignments/assignments.html", {
        "assignments": assignments,
        "submitted_ids": submitted_ids
    })
def assignment_list(request):
    if "user_id" not in request.session:
        return redirect("student_login")

    student = Student.objects.get(id=request.session["user_id"])

    enrollments = Enrollment.objects.filter(student=student)

    enrolled_ids = enrollments.values_list("course_id", flat=True)

    assignments = Assignment.objects.filter(course_id__in=enrolled_ids)

    submitted_ids = Submission.objects.filter(
        student=student
    ).values_list("assignment_id", flat=True)

    return render(request, "assignments/assignment_list.html", {
        "assignments": assignments,
        "submitted_ids": submitted_ids
    })