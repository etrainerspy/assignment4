# Generated by Django 5.0.6 on 2024-06-27 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_author_birth_year_author_firstname_author_lastname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='name',
        ),
    ]