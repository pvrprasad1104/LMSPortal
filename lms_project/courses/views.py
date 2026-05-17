from django.shortcuts import render, redirect, get_object_or_404
from courses.models import Course
from enrollments.models import Enrollment
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from datetime import datetime
from accounts.models import Student

def create_course(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")

    if request.method == "POST":
        Course.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description")
        )
        return redirect("admin_dashboard")

    return render(request, "courses/create_course.html")
def edit_course(request, course_id):
    if "admin_id" not in request.session:
        return redirect("admin_login")

    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        course.title = request.POST.get("title")
        course.description = request.POST.get("description")
        course.save()
        return redirect("admin_dashboard")

    return render(request, "courses/edit_course.html", {"course": course})
def delete_course(request, course_id):
    if "admin_id" not in request.session:
        return redirect("admin_login")

    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect("admin_dashboard")

def course_detail(request, id):
    course = get_object_or_404(Course, id=id)

    enrolled = False

    if "user_id" in request.session:
        user_id = request.session["user_id"]
        enrolled = Enrollment.objects.filter(
            student_id=user_id,
            course=course
        ).exists()

    return render(request, "courses/course_detail.html", {
        "course": course,
        "enrolled": enrolled
    })


# COURSE LIST
def course_list(request):

    courses = Course.objects.all()

    return render(request, "courses/course_list.html", {
        "courses": courses
    })

def generate_certificate(request, course_id):

    student_id = request.session.get("user_id")

    if not student_id:
        return HttpResponse("Login required")

    student = Student.objects.get(id=student_id)
    course = Course.objects.get(id=course_id)

    # check enrollment
    try:
        enrollment = Enrollment.objects.get(student=student, course=course)
    except Enrollment.DoesNotExist:
        return HttpResponse("You are not enrolled in this course")

    # ✅ FIX: use progress instead of is_completed
    if enrollment.progress < 100:
        return HttpResponse("You must complete the course to download certificate")

    # PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{course.title}.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(300, 500, "CERTIFICATE")

    p.setFont("Helvetica", 14)
    p.drawCentredString(300, 440, "This certifies that")

    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(300, 400, student.name)

    p.setFont("Helvetica", 14)
    p.drawCentredString(300, 360, "has completed the course")

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(300, 320, course.title)

    p.showPage()
    p.save()

    return response