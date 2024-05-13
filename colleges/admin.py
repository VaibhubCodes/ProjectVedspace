# colleges/admin.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django import forms
from .models import College
from .forms import CSVUploadForm
import csv
from .admin_mixins import AjaxSearchMixin

@admin.register(College)
class CollegeAdmin(AjaxSearchMixin, admin.ModelAdmin):
    list_display = ('name', 'university')
    search_fields = ('name',)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload-csv/', self.admin_site.admin_view(self.upload_csv), name='upload-csv'),
        ]
        return my_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            header = next(reader)  # Skip the header row.
            for row in reader:
                College.objects.create(
                    name=row[0],
                    university=row[1],
                    
                )
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CSVUploadForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)
