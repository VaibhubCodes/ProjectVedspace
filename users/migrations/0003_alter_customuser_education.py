# Generated by Django 5.0 on 2024-05-08 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_customuser_social_profiles_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='education',
            field=models.CharField(blank=True, choices=[('BTECH', 'B.Tech'), ('BCA', 'BCA'), ('BBA', 'BBA'), ('MCA', 'MCA'), ('MBA', 'MBA'), ('BSC', 'B.Sc.'), ('BDES', 'B.Des')], max_length=50, null=True),
        ),
    ]