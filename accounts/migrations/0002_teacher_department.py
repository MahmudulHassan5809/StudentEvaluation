# Generated by Django 2.2 on 2020-02-25 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0003_auto_20200225_1248'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='department_teacher', to='programs.Department'),
            preserve_default=False,
        ),
    ]
