from django.core.management.base import BaseCommand
import csv
from colleges.models import College

class Command(BaseCommand):
    help = 'Loads data from CSV into College model'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', type=str, help='The CSV file path')

    def handle(self, *args, **kwargs):
        csv_filename = kwargs['csv_filename']
        with open(csv_filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                College.objects.create(
                    name=row['name'],
                    location=row['location'],
                    ranking=int(row['ranking']),
                    description=row['description']
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded colleges from "%s"' % csv_filename))
