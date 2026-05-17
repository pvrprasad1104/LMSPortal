from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import home, dashboard, admin_dashboard, logout, profile, profile_update,add_student

from courses.views import (
    course_list, course_detail,
    create_course, edit_course, delete_course,
    generate_certificate
)

from enrollments.views import enroll_course, unenroll_course

from quizzes.views import (
    quiz_list, take_quiz, my_results,
    leaderboard, add_question,
    create_quiz, edit_question, delete_question
)

from assignments.views import (
    assignments, submit_assignment,
    view_submissions, give_marks,
    create_assignment, assignment_list
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", home, name="home"),

    path("dashboard/", dashboard, name="dashboard"),
    path("admin_dashboard/", admin_dashboard, name="admin_dashboard"),
    path("add_student/",add_student,name="add_student"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("profile_update/", profile_update, name="profile_update"),

    # Courses
    path("course_list/", course_list, name="course_list"),
    path("course/<int:id>/", course_detail, name="course_detail"),
    path("create_course/", create_course, name="create_course"),
    path("edit_course/<int:course_id>/", edit_course, name="edit_course"),
    path("delete_course/<int:course_id>/", delete_course, name="delete_course"),
    path("certificate/<int:course_id>/", generate_certificate, name="certificate"),

    # Enrollments
    path("enroll_course/<int:course_id>/", enroll_course, name="enroll_course"),
    path("unenroll/<int:course_id>/", unenroll_course, name="unenroll_course"),

    # Quizzes
    path("quiz_list/", quiz_list, name="quiz_list"),
    path("take_quiz/<int:quiz_id>/", take_quiz, name="take_quiz"),
    path("my_results/", my_results, name="my_results"),
    path("leaderboard/", leaderboard, name="leaderboard"),

    path("add_question/", add_question, name="add_question"),
    path("create_quiz/", create_quiz, name="create_quiz"),
    path("edit_question/<int:id>/", edit_question, name="edit_question"),
    path("delete_question/<int:id>/", delete_question, name="delete_question"),

    # Assignments
    path("assignment_list/", assignment_list, name="assignment_list"),
    path("assignments/", assignments, name="assignments"),
    path("submit_assignment/<int:assignment_id>/", submit_assignment, name="submit_assignment"),
    path("submissions/", view_submissions, name="view_submissions"),
    path("give_marks/<int:submission_id>/", give_marks, name="give_marks"),
    path("create_assignment/", create_assignment, name="create_assignment"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)