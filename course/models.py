from django.db import models
from django.utils.html import escape, mark_safe
from programs.models import Department
from accounts.models import Teacher, Student
from session.models import Semester


# Create your models here.


class Course(models.Model):
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, related_name='semester_courses')
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='department_courses')
    course_name = models.CharField(max_length=150)
    course_code = models.CharField(max_length=150)
    course_image = models.ImageField(upload_to="course/%Y/%m/%d/",default="course/default.png")
    course_credit = models.IntegerField()

    def __str__(self):
        return self.course_name


class AssignTeacher(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='course_teacher')
    teachers = models.ManyToManyField(Teacher, related_name='teacher_courses')

    def course_teachers(self):
        return ",".join([str(p) for p in self.teachers.all()])

    def __str__(self):
        return self.course.course_name


class StudentCourse(models.Model):
    courses = models.ManyToManyField(Course, related_name='student_courses')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_course')
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, related_name='semester_student_course')
    active = models.BooleanField(default=False)

    def courses_name(self):
        return ",".join([str(p) for p in self.courses.all()])

    def teachers_name(self):
        for course in self.courses.all():
            for course in course.course_teacher.all():
                return ",".join([str(teacher) for teacher in course.teachers.all()])

    def __str__(self):
        return self.student.student.username


class EvaluateStudent(models.Model):
    RATING = (
        ('1', 'Poor'),
        ('2', 'Average'),
        ('3', 'Good'),
        ('4', 'Very Good'),
        ('5', 'Excellent')
    )

    CHOICES = (
        ('1', 'Yes'),
        ('2', 'Average'),
        ('3', 'No')
    )

    QUESTIONS = (
        ('1', 'Does the student participate fully in discussions and class activity?'),
        ('2', 'Does the student thoughtfully participate in projects?'),
        ('3', 'Is the student regular and punctual in class?')
    )

    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='teacher_evaluate')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_evaluate')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='course_evaluate')
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, related_name='semester_evaluate')
    question1 = models.CharField(max_length=255, choices=CHOICES, default='2')
    question2 = models.CharField(max_length=255, choices=CHOICES, default='2')
    question3 = models.CharField(max_length=255, choices=CHOICES, default='2')

    rating = models.CharField(max_length=150, choices=RATING, default='3')
    review = models.TextField(default='Review')

    def __str__(self):
        return self.teacher.teacher.username

    def review_details(self):
        results = []
        for count, item in enumerate(self.QUESTIONS):
            if count == 0:
                results.append(f'{item[1]} --> {self.get_question1_display()}')
            if count == 1:
                results.append(f'{item[1]} --> {self.get_question2_display()}')
            if count == 2:
                results.append(f'{item[1]} --> {self.get_question3_display()}')

        return mark_safe("<br>".join(p for p in results))

    # answers_to_queations.allow_tags = True
