# quiz/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    timer = models.PositiveIntegerField(help_text="Duration in seconds")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(default=timezone.make_aware(timezone.datetime(2000, 1, 1, 23, 0)))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes')
    questions = models.ManyToManyField(Question, related_name='quizzes', blank=True)

    def __str__(self):
        return self.title

class UserQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='user_quizzes')
    score = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def duration(self):
        return (self.end_time - self.start_time).total_seconds() if self.end_time else None

    def is_time_expired(self):
        if self.end_time:
            return False
        time_elapsed = (timezone.now() - self.start_time).total_seconds()
        return time_elapsed > self.quiz.timer

    def __str__(self):
        return f"{self.user.phone_number} - {self.quiz.title}"
