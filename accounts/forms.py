from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from programs.models import Faculty,Department

class SignUpForm(UserCreationForm):
	USERTYPE_CHOICES = (
	    ('0', 'Teacher'),
	    ('1', 'Student'),
	)

	phone_number = forms.CharField()
	address = forms.CharField()
	bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
	user_type = forms.ChoiceField(choices = USERTYPE_CHOICES) 
	department = forms.ModelChoiceField(queryset=Department.objects.all())
	faculty = forms.ModelChoiceField(queryset=Faculty.objects.all())

	class Meta:
		model = User
		fields = ('username', 'first_name','last_name', 'email','phone_number','bio','address','user_type', 'password1', 'password2', )
	

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if not email.endswith('.edu'):
			raise forms.ValidationError("Only .edu email addresses allowed")
		return email	
	
	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		for fieldname in ['username', 'password1', 'password2']:
			self.fields[fieldname].help_text = None
			self.fields['email'].required = True
			self.fields['first_name'].required = True
			self.fields['last_name'].required = True






class LoginForm(forms.Form):
	username =  forms.CharField(label='Your username', required=True)
	password = forms.CharField(widget=forms.PasswordInput())