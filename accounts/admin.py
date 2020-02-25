from django.contrib import admin
from django.utils.html import escape, mark_safe
from .models import Profile,Teacher,Student
from django.contrib.auth.models import User

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
	list_display = ["profile_name","user_type","phone_number","address","user_email","profile_pic","active","add_teacher_or_student"]
	search_fields = ('user__username','phone_number',)
	list_filter = ['phone_number','user__email']
	list_editable = ['active']
	list_per_page = 20



	def add_teacher_or_student(self,obj):
		if obj.user_type == '0':
			return mark_safe(f'<a target="_blank" href="http://127.0.0.1:8000/admin/accounts/teacher/add/?type={obj.user.id}">Add To Teacher</a>')
		if obj.user_type == '1':
			return mark_safe(f'<a target="_blank" href="http://127.0.0.1:8000/admin/accounts/student/add/?type={obj.user.id}">Add To Student</a>')



	def profile_name(self,obj):
		return obj.user.username

	def user_email(self,obj):
		return obj.user.email

admin.site.register(Profile,ProfileAdmin)



class TeacherAdmin(admin.ModelAdmin):
	list_display = ["teacher_name","phone_number","user_email"]
	search_fields = ('teacher__username','teacher__user_profile__phone_number','teacher__user_profile__email',)
	list_filter = ['teacher__user_profile__active']
	list_per_page = 20


	def teacher_name(self,obj):
		return obj.teacher.username

	def phone_number(self,obj):
		return obj.teacher.user_profile.phone_number

	def user_email(self,obj):
		return obj.teacher.email

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		id = request.GET.get('type')
		if db_field.name == 'teacher' and id:
			kwargs["queryset"] = User.objects.filter(id=int(id))
			return super().formfield_for_foreignkey(db_field, request, **kwargs)
		elif db_field.name == 'teacher':
			kwargs["queryset"] = User.objects.filter(user_profile__user_type='0')
			return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Teacher,TeacherAdmin)



class StudentAdmin(admin.ModelAdmin):
	list_display = ["student_name","phone_number","user_email"]
	search_fields = ('student__username','student__user_profile__phone_number','student__user_profile__email',)
	list_filter = ['student__user_profile__active']
	list_per_page = 20


	def student_name(self,obj):
		return obj.student.username

	def phone_number(self,obj):
		return obj.student.user_profile.phone_number

	def user_email(self,obj):
		return obj.student.email

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		id = request.GET.get('type')
		if db_field.name == 'student' and id:
			kwargs["queryset"] = User.objects.filter(id=int(id),user_profile__user_type='1')
			return super().formfield_for_foreignkey(db_field, request, **kwargs)
		elif db_field.name == 'student':
			kwargs["queryset"] = User.objects.filter(user_profile__user_type='1')
			return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Student,StudentAdmin)