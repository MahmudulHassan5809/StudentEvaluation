from django.db import models
from programs.models import Department
from accounts.models import Teacher
from session.models import Semester

# Create your models here.
class Course(models.Model):
	semester   =  models.ForeignKey(Semester,on_delete=models.CASCADE,related_name='semester_courses')
	department   =  models.ForeignKey(Department,on_delete=models.CASCADE,related_name='department_courses')
	course_name  =  models.CharField(max_length=150)
	course_code  =  models.CharField(max_length=150)
	course_image =  models.ImageField(upload_to="course/%Y/%m/%d/")
	course_credit = models.IntegerField()

	def __str__(self):
		return self.course_name



class AssignTeacher(models.Model):
	course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='course_teacher')
	teacher =  models.ManyToManyField(Teacher,related_name='teacher_courses')


	def course_teachers(self):
		return ",".join([str(p) for p in self.teacher.all()])


	def __str__(self):
		return self.course.course_name

