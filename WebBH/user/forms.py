from pyexpat import model
from django import forms
from .models import *
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','hoten','gioitinh','dienthoai','diachi']

class UserPassForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']
class UserImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']