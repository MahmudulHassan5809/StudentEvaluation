from django.db import models
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
    course_image = models.ImageField(upload_to="course/%Y/%m/%d/")
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
