from django import forms
from django.forms import ModelForm
from .models import City


class WeatherCityForm(ModelForm):
    class Meta:
        model = City
        fields = ('city',)
