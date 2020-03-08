from django import forms
from django.forms import ModelForm
from django.forms import MultipleChoiceField
from course.models import Course, StudentCourse, EvaluateStudent
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


class EvaluateForm(ModelForm):
    # QUESTION_CHOICES = [
    #     ('Does the student participate fully in discussions and class activity?',
    #      (('1', 'Yes'), ('2', 'Average'), ('2', 'No'),)),
    #     ('Does the student thoughtfully participate in projects?',
    #      (('1', 'Yes'), ('2', 'Average'), ('2', 'No'),)),
    #     ('Is the student regular and punctual in class?', (('1', 'Yes'), ('2', 'Average'), ('2', 'No'),)), ]

    # CHOICES = (
    #     ('1', 'Yes'),
    #     ('2', 'Average'),
    #     ('3', 'No')
    # )

    review = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    # question1 = forms.ChoiceField(
    #     choices=QUESTION_CHOICES, widget=forms.RadioSelect())
    # question2 = forms.ChoiceField(
    #     choices=QUESTION_CHOICES, widget=forms.RadioSelect())
    # question3 = forms.ChoiceField(
    #     choices=QUESTION_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = EvaluateStudent
        fields = ('teacher', 'student', 'course',
                  'question1', 'question2', 'question3', 'review', 'rating',)
        # widgets = {
        #     'question': forms.RadioSelect(attrs={"required": "required"}),
        # }

    def __init__(self, *args, **kwargs):
        student_obj = kwargs.pop('student_obj', None)
        teacher_obj = kwargs.pop('teacher_obj', None)
        course_obj = kwargs.pop('course_obj', None)
        super(EvaluateForm, self).__init__(*args, **kwargs)

        if student_obj:
            self.fields['student'].initial = student_obj
        if teacher_obj:
            self.fields['teacher'].initial = teacher_obj
        if course_obj:
            self.fields['course'].initial = course_obj

        self.fields['question1'].label = "Does the student participate fully in discussions and class activity?"
        self.fields['question2'].label = "Does the student thoughtfully participate in projects?"
        self.fields['question3'].label = "Is the student regular and punctual in class?"
