# Generated by Django 2.2 on 2020-03-07 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0001_initial'),
        ('accounts', '0003_profile_email_confirmed'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='teacher',
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('courses', models.ManyToManyField(related_name='student_courses', to='course.Course')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semester_student_course', to='session.Semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_course', to='accounts.Student')),
            ],
        ),
        migrations.CreateModel(
            name='EvaluateStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=150, null=True)),
                ('rating', models.CharField(choices=[(1, 'Poor'), (2, 'Average'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')], default=3, max_length=150)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_evaluate', to='course.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_evaluate', to='accounts.Student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_evaluate', to='accounts.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='AssignTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_teacher', to='course.Course')),
                ('teachers', models.ManyToManyField(related_name='teacher_courses', to='accounts.Teacher')),
            ],
        ),
    ]