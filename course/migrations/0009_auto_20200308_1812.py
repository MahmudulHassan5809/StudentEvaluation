# Generated by Django 2.2 on 2020-03-08 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_auto_20200307_1954'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evaluatestudent',
            old_name='question',
            new_name='question1',
        ),
        migrations.AddField(
            model_name='evaluatestudent',
            name='question2',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='evaluatestudent',
            name='question3',
            field=models.CharField(default='', max_length=255),
        ),
    ]
