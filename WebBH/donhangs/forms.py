from pyexpat import model
from django import forms
from . models import *
class DonHangForm(forms.ModelForm):
    class Meta:
        model = DonHang
        fields = "__all__"
