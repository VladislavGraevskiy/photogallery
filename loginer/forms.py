from django.forms import ModelForm
from django import forms
from loginer.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6, max_length=32)
