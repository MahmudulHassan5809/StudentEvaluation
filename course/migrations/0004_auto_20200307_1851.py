# Generated by Django 2.2 on 2020-03-07 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_evaluatestudent_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluatestudent',
            name='question',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='evaluatestudent',
            name='rating',
            field=models.CharField(choices=[('1', 'Poor'), ('2', 'Average'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')], default='3', max_length=150),
        ),
    ]