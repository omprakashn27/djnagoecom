from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm 
from .models import User
from django import forms

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter Username'}))
    email = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter your Email address'}))
    password1 = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter Your Password'}))
    password2 = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Confirm Password'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
