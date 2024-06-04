# quiz/utils.py

import csv
from .models import Category, Question, Option

def import_questions_from_csv(file):
    reader = csv.reader(file)
    for row in reader:
        if len(row) < 7:
            continue  # Ensure row has enough columns

        category_name, question_text, option1, option2, option3, option4, correct_option = row

        # Get or create category
        category, created = Category.objects.get_or_create(name=category_name)

        # Create question
        question = Question.objects.create(
            text=question_text,
            category=category,
        )

        # Create options
        options = [option1, option2, option3, option4]
        for i, option_text in enumerate(options, start=1):
            Option.objects.create(
                question=question,
                text=option_text,
                is_correct=(str(i) == correct_option),
            )
