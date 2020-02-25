from django.contrib import admin
from .models import Semester

# Register your models here.
class SemesterAdmin(admin.ModelAdmin):
	list_display = ["semester_name","semester_year","semester_full_name","active"]
	search_fields = ('semester_name','semester_year','semester_full_name',)
	list_filter = ['active','semester_full_name']
	list_editable = ['active']
	exclude = ['semester_full_name']
	list_per_page = 20

admin.site.register(Semester,SemesterAdmin)