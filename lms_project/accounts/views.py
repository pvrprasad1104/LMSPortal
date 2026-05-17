from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from accounts.models import Student, StudentProfile, AdminUser
from courses.models import Course
from enrollments.models import Enrollment
from quizzes.models import Result, Question, Quiz
from assignments.models import Submission
import random


# ---------------- HOME (ALL LOGIN/SIGNUP HERE) ----------------
def home(request):

    if request.method == "POST":

        action = request.POST.get("action")

        # ================= STUDENT LOGIN =================
        if action == "student_login":

            user = Student.objects.filter(
                username=request.POST.get("username"),
                password=request.POST.get("password")
            ).first()

            if user:
                request.session.flush()
                request.session["user_id"] = user.id
                request.session["role"] = "student"
                return redirect("dashboard")

            return HttpResponse("Invalid Student Login")

        # ================= STUDENT SIGNUP =================
        elif action == "student_signup":
            username = request.POST.get("username")
            if Student.objects.filter(username=username).exists():
                return HttpResponse("Student already exists")
            otp = random.randint(1000, 9999)
            request.session["temp_student"] = {
                "username": username,
                "name": request.POST.get("name"),
                "email": request.POST.get("email"),
                "phone": request.POST.get("phone"),
                "password": request.POST.get("password"),
                "otp": otp
                }
            send_mail(
                "LMS Verification OTP",
                f"Your OTP is {otp}",
                "lms@gmail.com",
                [request.POST.get("email")],
                fail_silently=False
                )
            return redirect("verify_student_page")

        # ================= VERIFY STUDENT =================
        elif action == "verify_student":

            temp = request.session.get("temp_student")

            if temp and str(request.POST.get("otp")) == str(temp["otp"]):

                Student.objects.create(
                    username=temp["username"],
                    name=temp["name"],
                    email=temp["email"],
                    phone=temp["phone"],
                    password=temp["password"]
                )

                del request.session["temp_student"]

                return HttpResponse("Student Created Successfully")

            return HttpResponse("Invalid OTP")

        # ================= ADMIN LOGIN =================
        elif action == "admin_login":

            admin = AdminUser.objects.filter(
                username=request.POST.get("username"),
                password=request.POST.get("password")
            ).first()

            if admin:
                request.session.flush()
                request.session["admin_id"] = admin.id
                request.session["role"] = "admin"
                return redirect("admin_dashboard")

            return HttpResponse("Invalid Admin Login")

        # ================= ADMIN SIGNUP =================
        elif action == "admin_signup":

            username = request.POST.get("username")

            if AdminUser.objects.filter(username=username).exists():
                return HttpResponse("Admin already exists")

            otp = random.randint(1000, 9999)

            request.session["temp_admin"] = {
                "username": username,
                "password": request.POST.get("password"),
                "otp": otp
            }

            return render(request, "accounts/home.html", {"admin_otp": otp})

        # ================= VERIFY ADMIN =================
        elif action == "verify_admin":

            temp = request.session.get("temp_admin")

            if temp and str(request.POST.get("otp")) == str(temp["otp"]):

                AdminUser.objects.create(
                    username=temp["username"],
                    password=temp["password"]
                )

                del request.session["temp_admin"]

                return HttpResponse("Admin Created Successfully")

            return HttpResponse("Invalid OTP")

    return render(request, "accounts/home.html")


# ---------------- DASHBOARD ----------------
def dashboard(request):

    if "user_id" not in request.session:
        return redirect("home")

    student = Student.objects.get(id=request.session["user_id"])

    enrollments = Enrollment.objects.filter(student=student)
    quiz_results = Result.objects.filter(student=student)
    submitted_ids = Submission.objects.filter(student=student).values_list("assignment_id", flat=True)

    return render(request, "accounts/dashboard.html", {
        "student": student,
        "enrollments": enrollments,
        "quiz_results": quiz_results,
        "submitted_ids": submitted_ids,
    })


# ---------------- ADMIN DASHBOARD ----------------
def admin_dashboard(request):

    quizzes = Quiz.objects.all()
    questions = Question.objects.all()
    students = Student.objects.all()
    results = Result.objects.all()
    courses = Course.objects.all()

    return render(request, "accounts/admin_dashboard.html", {
        "quizzes": quizzes,
        "questions": questions,
        "students": students,
        "results": results,
        "courses": courses
    })


# ---------------- LOGOUT ----------------
def logout(request):
    request.session.flush()
    return redirect("home")


# ---------------- PROFILE ----------------
def profile(request):

    if "user_id" not in request.session:
        return redirect("home")

    student = Student.objects.get(id=request.session["user_id"])

    return render(request, "accounts/profile.html", {
        "student": student
    })


# ---------------- PROFILE UPDATE ----------------
def profile_update(request):

    if "user_id" not in request.session:
        return redirect("home")

    user = Student.objects.get(id=request.session["user_id"])

    if request.method == "POST":

        StudentProfile.objects.update_or_create(
            user=user,
            defaults={
                "bio": request.POST.get("bio"),
                "address": request.POST.get("address"),
                "city": request.POST.get("city"),
                "state": request.POST.get("state"),
                "pincode": request.POST.get("pincode"),
                "country": request.POST.get("country"),
                "profile_pic": request.FILES.get("profile_pic"),
                "resume": request.FILES.get("resume"),
            }
        )

        return redirect("profile")

    return render(request, "accounts/profile_update.html")

def add_student(request):

    if "admin_id" not in request.session:
        return redirect("home")

    if request.method == "POST":

        Student.objects.create(
            username=request.POST.get("username"),
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            password=request.POST.get("password")
        )

        return redirect("admin_dashboard")

    return render(request, "accounts/add_student.html")