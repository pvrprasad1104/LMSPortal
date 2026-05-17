from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from reportlab.pdfgen import canvas

from .models import Quiz, Question, Result
from accounts.models import Student


# ---------------- QUIZ LIST ----------------
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, "quizzes/quiz_list.html", {"quizzes": quizzes})


# ---------------- TAKE QUIZ ----------------
def take_quiz(request, quiz_id):

    if "user_id" not in request.session:
        return redirect("student_login")

    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return HttpResponse("Quiz not found")

    # deadline check
    if quiz.deadline and timezone.now() > quiz.deadline:
        return HttpResponse("⛔ Quiz deadline is over")

    questions = Question.objects.filter(quiz=quiz)
    student = Student.objects.get(id=request.session["user_id"])

    # ---------------- SUBMIT QUIZ ----------------
    if request.method == "POST":

        score = 0

        for q in questions:
            selected = request.POST.get(str(q.id))

            # map A/B/C/D to actual options
            correct_map = {
                "A": q.option1,
                "B": q.option2,
                "C": q.option3,
                "D": q.option4
            }

            # compare selected answer
            if selected and correct_map.get(selected) == q.correct_option:
                score += 1

        total = questions.count()
        percentage = (score / total) * 100 if total > 0 else 0

        Result.objects.create(
            student=student,
            quiz=quiz,
            score=score,
            total=total,
            percentage=percentage
        )

        return render(request, "quizzes/result.html", {
            "score": score,
            "total": total,
            "percentage": round(percentage, 2)
        })

    # ---------------- SHOW QUIZ ----------------
    return render(request, "quizzes/take_quiz.html", {
        "quiz": quiz,
        "questions": questions
    })


# ---------------- MY RESULTS ----------------
def my_results(request):

    if "user_id" not in request.session:
        return redirect("student_login")

    student = Student.objects.get(id=request.session["user_id"])
    results = Result.objects.filter(student=student)

    return render(request, "quizzes/my_results.html", {
        "results": results
    })


# ---------------- LEADERBOARD ----------------
def leaderboard(request):

    results = Result.objects.select_related("student", "quiz")

    leaderboard_data = {}

    for r in results:
        sid = r.student.id

        if sid not in leaderboard_data:
            leaderboard_data[sid] = {
                "student": r.student,
                "score": r.score
            }
        else:
            leaderboard_data[sid]["score"] = max(
                leaderboard_data[sid]["score"],
                r.score
            )

    leaderboard_list = list(leaderboard_data.values())
    leaderboard_list.sort(key=lambda x: x["score"], reverse=True)

    return render(request, "quizzes/leaderboard.html", {
        "leaderboard": leaderboard_list
    })


# ---------------- CERTIFICATE ----------------
def download_certificate(request, quiz_id):

    if "user_id" not in request.session:
        return redirect("student_login")

    student = Student.objects.get(id=request.session["user_id"])
    quiz = Quiz.objects.get(id=quiz_id)

    result = Result.objects.filter(student=student, quiz=quiz).first()

    if not result:
        return HttpResponse("You have not completed this quiz")

    if result.percentage < 50:
        return HttpResponse("You are not eligible for certificate")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{quiz.title}.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(300, 750, "CERTIFICATE OF COMPLETION")

    p.setFont("Helvetica", 14)
    p.drawCentredString(300, 700, f"This certifies that {student.name}")

    p.drawCentredString(300, 670, "has successfully completed the quiz")

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(300, 640, quiz.title)

    p.setFont("Helvetica", 12)
    p.drawCentredString(300, 610, f"Score: {result.score}/{result.total}")

    p.save()

    return response


# ---------------- ADD QUESTION ----------------
def add_question(request):

    if "admin_id" not in request.session:
        return redirect("admin_login")

    quizzes = Quiz.objects.all()

    if request.method == "POST":
        Question.objects.create(
            quiz_id=request.POST.get("quiz"),
            question_text=request.POST.get("question"),
            option1=request.POST.get("option1"),
            option2=request.POST.get("option2"),
            option3=request.POST.get("option3"),
            option4=request.POST.get("option4"),
            correct_option=request.POST.get("correct")  # A/B/C/D or text (your choice)
        )
        return redirect("admin_dashboard")

    return render(request, "quizzes/add_question.html", {
        "quizzes": quizzes
    })


# ---------------- CREATE QUIZ ----------------
def create_quiz(request):

    if "admin_id" not in request.session:
        return redirect("admin_login")

    if request.method == "POST":
        Quiz.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            deadline=request.POST.get("deadline")
        )
        return redirect("admin_dashboard")

    return render(request, "quizzes/create_quiz.html")


# ---------------- DELETE QUESTION ----------------
def delete_question(request, id):

    if "admin_id" not in request.session:
        return redirect("admin_login")

    Question.objects.filter(id=id).delete()
    return redirect("admin_dashboard")


# ---------------- EDIT QUESTION ----------------
def edit_question(request, id):

    if "admin_id" not in request.session:
        return redirect("admin_login")

    q = Question.objects.get(id=id)

    if request.method == "POST":
        q.question_text = request.POST.get("question")
        q.option1 = request.POST.get("option1")
        q.option2 = request.POST.get("option2")
        q.option3 = request.POST.get("option3")
        q.option4 = request.POST.get("option4")
        q.correct_option = request.POST.get("correct")
        q.save()

        return redirect("admin_dashboard")

    return render(request, "quizzes/edit_question.html", {"q": q})