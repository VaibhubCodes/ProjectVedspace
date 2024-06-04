# quiz/forms.py

from django import forms
from .models import Quiz, Question, Category

class QuestionCSVForm(forms.Form):
    csv_file = forms.FileField()

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].queryset = Question.objects.filter(category=self.instance.category)
        else:
            self.fields['questions'].queryset = Question.objects.none()
