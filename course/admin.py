from django.contrib import admin
from .models import Course
from session.models import Semester
from programs.models import Department

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
	list_display = ["course_name","course_code","course_teachers","course_credit","semester","department"]
	search_fields = ('course_name','course_code','teacher','semester','department',)
	list_filter = ['course_credit','course_code','department','semester']
	autocomplete_fields = ('department','teacher',)
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