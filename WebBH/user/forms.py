from pyexpat import model
from django import forms
from .models import *
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class UserImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']