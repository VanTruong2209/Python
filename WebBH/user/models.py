from django.db import models

# Create your models here.
class User(models.Model):
    id_user = models.IntegerField(primary_key=True,null=False)
    username = models.CharField(max_length=100,null=False)
    password = models.CharField(max_length=100,null=False)
    hoten = models.CharField(max_length=100)
    gioitinh = models.BooleanField(default=True)
    diachi = models.CharField(max_length=100)
    dienthoai =  models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    quyen = models.BooleanField(default=True)