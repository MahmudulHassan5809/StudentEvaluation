from django.contrib import admin
from .models import Course,AssignTeacher
from session.models import Semester
from programs.models import Department

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
	list_display = ["course_name","course_code","course_credit","semester","department"]
	search_fields = ('course_name','course_code','semester__semester_name','department__department_name',)
	list_filter = ['course_credit','course_code','department__department_name','semester__semester_name']
	autocomplete_fields = ('department',)
	#raw_id_fields = ("teacher",)
	list_per_page = 20


	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'semester':
			kwargs["queryset"] = Semester.objects.filter(active=True)
			return super().formfield_for_foreignkey(db_field, request, **kwargs)
		if db_field.name == 'department':
			kwargs["queryset"] = Department.objects.all()
			return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Course,CourseAdmin)



class AssignTeacherAdmin(admin.ModelAdmin):
	list_display = ["course","course_teachers","department","faculty","semester"]
	search_fields = ('course__course_name','course__course_code','teacher__teacher__username','course__semester__semester_name','course__department__department_name',)
	list_filter = ['course__course_credit','course__course_code','course__department__department_name','course__semester__semester_full_name']
	autocomplete_fields = ('course','teacher',)
	#raw_id_fields = ("teacher",)
	list_per_page = 20


	def department(self,obj):
		return obj.course.department.department_name

	def faculty(self,obj):
		return obj.course.department.faculty.faculty_name

	def semester(self,obj):
		return obj.course.semester.semester_full_name

admin.site.register(AssignTeacher,AssignTeacherAdmin)