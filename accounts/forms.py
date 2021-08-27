from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from accounts.models import *


class CreateTaskForm(ModelForm):
    class Meta:
        model = Bucket
        fields = ['name', 'task']



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        #if it works, i changed from [] to ()
        fields = ('email', 'username', 'password1', 'password2')


class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    # overriding the original method is causing the error
    def clean(self):
        email = self.data.get('email')
        password = self.data.get('password')
        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Invalid Login')