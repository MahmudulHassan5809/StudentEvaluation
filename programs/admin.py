from django.contrib import admin
from .models import Faculty,Department

# Register your models here.
class FacultyAdmin(admin.ModelAdmin):
	list_display = ["faculty_name"]
	search_fields = ('faculty_name',)
	list_per_page = 20

admin.site.register(Faculty,FacultyAdmin)



class DepartmentAdmin(admin.ModelAdmin):
	list_display = ["department_name","faculty"]
	search_fields = ('department_name','faculty__faculty_name',)
	list_per_page = 20

admin.site.register(Department,DepartmentAdmin)