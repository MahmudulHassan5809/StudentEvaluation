# Generated by Django 2.2 on 2020-03-05 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_studentcourse_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcourse',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]