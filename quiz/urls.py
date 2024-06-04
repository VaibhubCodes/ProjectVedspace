# quiz/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('quizzes/<int:pk>/start/', views.start_quiz, name='start_quiz'),
    path('quizzes/<int:pk>/submit/', views.submit_quiz, name='submit_quiz'),
    path('quizzes/<int:quiz_id>/leaderboard/', views.leaderboard, name='leaderboard'),
    path('quizzes/auto_submit/<int:user_quiz_id>/', views.auto_submit_quiz, name='auto_submit_quiz'),
]
