from django import forms
from django.forms import ModelForm
from django.forms import MultipleChoiceField
from course.models import Course, StudentCourse
from session.models import Semester


class CourseChoiceForm(ModelForm):
    class Meta:
        model = StudentCourse
        exclude = ['student']

    # courses = forms.ModelMultipleChoiceField(
    #     queryset=Course.objects.filter(semester__active=True))

    def __init__(self, *args, **kwargs):
        # call the parent init
        super(CourseChoiceForm, self).__init__(*args, **kwargs)
        # change the widget to use checkboxes
        self.fields['courses'] = forms.ModelMultipleChoiceField(
            queryset=Course.objects.filter(semester__active=True),
            required=True,
            widget=forms.CheckboxSelectMultiple)
        self.fields['semester'] = forms.ModelChoiceField(
            queryset=Semester.objects.filter(active=True))
