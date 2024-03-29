from django.contrib import admin
from django.utils.html import escape, mark_safe
from .models import Course, AssignTeacher, StudentCourse, EvaluateStudent
from session.models import Semester
from programs.models import Department

# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_display = ["course_name", "course_code",
                    "course_credit", "semester", "department"]
    search_fields = ('course_name', 'course_code',
                     'semester__semester_name', 'department__department_name',)
    list_filter = ['course_credit', 'course_code',
                   'department__department_name', 'semester__semester_full_name']
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


admin.site.register(Course, CourseAdmin)


class AssignTeacherAdmin(admin.ModelAdmin):
    list_display = ["course", "course_teachers",
                    "department", "faculty", "semester"]
    search_fields = ('course__course_name', 'course__course_code', 'teachers__teacher__username',
                     'course__semester__semester_name', 'course__department__department_name',)
    list_filter = ['course__course_credit', 'course__course_code',
                   'course__department__department_name', 'course__semester__semester_full_name']
    autocomplete_fields = ('course', 'teachers',)
    #raw_id_fields = ("teacher",)
    list_per_page = 20

    def department(self, obj):
        return obj.course.department.department_name

    def faculty(self, obj):
        return obj.course.department.faculty.faculty_name

    def semester(self, obj):
        return obj.course.semester.semester_full_name


admin.site.register(AssignTeacher, AssignTeacherAdmin)


class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ["courses_name", "teachers_name",
                    "semester", "student", "active"]
    search_fields = ["courses__course_name", "student__student__username"]
    list_filter = ["semester__semester_full_name"]
    list_editable = ["active"]
    list_per_page = 20


admin.site.register(StudentCourse, StudentCourseAdmin)


class EvaluateStudentAdmin(admin.ModelAdmin):
    list_display = ["teacher", "student", "course", "answers_to_queations"]
    list_per_page = 20

    def answers_to_queations(self, obj):
        results = []
        for count, item in enumerate(obj.QUESTIONS):
            if count == 0:
                results.append(f'{item[1]} --> {obj.get_question1_display()}')
            if count == 1:
                results.append(f'{item[1]} --> {obj.get_question2_display()}')
            if count == 2:
                results.append(f'{item[1]} --> {obj.get_question3_display()}')

        return mark_safe("<br>".join(p for p in results))

    answers_to_queations.allow_tags = True


admin.site.register(EvaluateStudent, EvaluateStudentAdmin)
