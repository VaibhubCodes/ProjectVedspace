# quiz/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Category, Quiz, Question, Option, UserQuiz

def quiz_list(request):
    categories = Category.objects.all()
    return render(request, 'quiz/quiz_list.html', {'categories': categories})

def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz})

def start_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    now = timezone.now()

    if now < quiz.start_time or now > quiz.end_time:
        return render(request, 'quiz/quiz_inactive.html', {'quiz': quiz})

    user_quiz, created = UserQuiz.objects.get_or_create(user=request.user, quiz=quiz, start_time=now)

    elapsed_time = (now - quiz.start_time).total_seconds()
    remaining_time = max(quiz.timer - elapsed_time, 0)

    return render(request, 'quiz/quiz_start.html', {'user_quiz': user_quiz, 'remaining_time': remaining_time})

def submit_quiz(request, pk):
    user_quiz = get_object_or_404(UserQuiz, pk=pk, user=request.user)
    if request.method == 'POST':
        if user_quiz.end_time is not None:
            return redirect('quiz_list')

        user_quiz.end_time = timezone.now()
        score = 0

        for question in user_quiz.quiz.questions.all():
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = Option.objects.get(id=selected_option_id)
                if selected_option.is_correct:
                    score += 2

        user_quiz.score = score
        user_quiz.save()
        return redirect('leaderboard', quiz_id=user_quiz.quiz.id)

    return render(request, 'quiz/quiz_submit.html', {'user_quiz': user_quiz})

def leaderboard(request, quiz_id):
    user_quizzes = UserQuiz.objects.filter(quiz__id=quiz_id)
    for user_quiz in user_quizzes:
        user_quiz.duration = (user_quiz.end_time - user_quiz.start_time).total_seconds() if user_quiz.end_time else float('inf')

    sorted_user_quizzes = sorted(user_quizzes, key=lambda uq: (-uq.score, uq.duration))
    for index, user_quiz in enumerate(sorted_user_quizzes):
        user_quiz.rank = index + 1

    return render(request, 'quiz/leaderboard.html', {'user_quizzes': sorted_user_quizzes})

def auto_submit_quiz(request, user_quiz_id):
    user_quiz = get_object_or_404(UserQuiz, pk=user_quiz_id, user=request.user)
    if user_quiz.end_time is None and user_quiz.is_time_expired():
        user_quiz.end_time = timezone.now()
        score = 0

        for question in user_quiz.quiz.questions.all():
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = Option.objects.get(id=selected_option_id)
                if selected_option.is_correct:
                    score += 2

        user_quiz.score = score
        user_quiz.save()

    return redirect('leaderboard', quiz_id=user_quiz.quiz.id)
