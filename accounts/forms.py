from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from programs.models import Faculty, Department


class SignUpForm(UserCreationForm):
    USERTYPE_CHOICES = (
        ('0', 'Teacher'),
        ('1', 'Student'),
    )

    phone_number = forms.CharField()
    address = forms.CharField()
    # bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    user_type = forms.ChoiceField(choices=USERTYPE_CHOICES)
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number',
                  'address', 'user_type', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('indstate.edu'):
            raise forms.ValidationError(
                "Only indstate.edu email addresses allowed")
        return email

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        self.fields['department'].label = "Program"
        self.fields['faculty'].label = "Department"


class LoginForm(forms.Form):
    username = forms.CharField(label='Your username', required=True)
    password = forms.CharField(widget=forms.PasswordInput())


class UpdateProfile(ModelForm):
    phone_number = forms.CharField()
    address = forms.CharField()
    # bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'address',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        user = self.request.user
        super(UpdateProfile, self).__init__(*args, **kwargs)

        self.fields['phone_number'].initial = user.user_profile.phone_number
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        # self.fields['bio'].initial = user.user_profile.bio
        self.fields['address'].initial = user.user_profile.address


class SendMailForm(forms.Form):
    mail_from = forms.CharField(required=True)
    mail_to = forms.CharField(required=True)
    mail_subject = forms.CharField(required=True)
    mail_message = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 9, 'cols': 40}), required=True)
    mail_attachment = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
