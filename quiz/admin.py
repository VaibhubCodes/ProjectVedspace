# quiz/admin.py

from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from .models import Category, Quiz, Question, Option, UserQuiz
from .forms import QuestionCSVForm, QuizForm
from .utils import import_questions_from_csv

class OptionInline(admin.TabularInline):
    model = Option

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ('text', 'category')
    list_filter = ('category',)
    change_list_template = "quiz/question_changelist.html"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='import_csv'),
        ]
        return custom_urls + urls
    
    def import_csv(self, request):
        if request.method == "POST":
            form = QuestionCSVForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES["csv_file"].read().decode('utf-8').splitlines()  # Read and decode the file content
                import_questions_from_csv(csv_file)
                self.message_user(request, "Questions imported successfully")
                return redirect("..")
        else:
            form = QuestionCSVForm()

        context = {
            "form": form,
            "opts": self.model._meta,
            "app_label": self.model._meta.app_label,
        }
        return render(request, "quiz/import_csv.html", context)

class QuizAdmin(admin.ModelAdmin):
    form = QuizForm
    list_display = ('title', 'category', 'start_time', 'end_time', 'timer')
    list_filter = ('category', 'start_time', 'end_time')

    def save_model(self, request, obj, form, change):
        if obj.pk:
            obj.questions.set(form.cleaned_data['questions'])
        else:
            obj.save()
            obj.questions.set(form.cleaned_data['questions'])

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.action(description='View Leaderboard')
def view_leaderboard(modeladmin, request, queryset):
    user_quizzes = list(queryset)
    for user_quiz in user_quizzes:
        user_quiz.duration = (user_quiz.end_time - user_quiz.start_time).total_seconds() if user_quiz.end_time else float('inf')

    sorted_user_quizzes = sorted(user_quizzes, key=lambda uq: (-uq.score, uq.duration))
    for index, user_quiz in enumerate(sorted_user_quizzes):
        user_quiz.rank = index + 1

    context = {'user_quizzes': sorted_user_quizzes}
    return render(request, 'quiz/leaderboard.html', context)

class UserQuizAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'start_time', 'end_time', 'get_duration')
    actions = [view_leaderboard]

    def get_duration(self, obj):
        return (obj.end_time - obj.start_time).total_seconds() if obj.end_time else None
    get_duration.short_description = 'Duration (seconds)'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserQuiz, UserQuizAdmin)
