from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField() 
    profile_image = forms.ImageField(required=False, widget=forms.ClearableFileInput)  

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_image']
