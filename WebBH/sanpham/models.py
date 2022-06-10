import datetime
from pyexpat import model
from django.db import models
from user.models import *
# Create your models here.
class LoaiSanPham(models.Model):
    id_loaisanpham = models.IntegerField(primary_key=True,null=False)
    tenloaisanpham = models.CharField(max_length=100)
    # hang = models.ForeignKey(Hang, on_delete=models.CASCADE,default=1)

class Hang(models.Model):
    id_hang = models.IntegerField(primary_key=True,null=False)
    tenhang = models.CharField(max_length=100)
    hinhanh = models.CharField(max_length=1000,null=True)
    loaisanpham = models.ForeignKey(LoaiSanPham, on_delete=models.CASCADE,default=1)

class SanPham(models.Model):
    id_sanpham = models.IntegerField(primary_key=True,null=False)
    loaisanpham = models.ForeignKey(LoaiSanPham, on_delete=models.CASCADE)
    tensanpham = models.CharField(max_length=500,null=True)
    hang = models.ForeignKey(Hang, on_delete=models.CASCADE)
    dongia = models.FloatField(default=0)
    soluong = models.IntegerField(default=0)
    mota = models.CharField(max_length=10000)
    hinhanh = models.CharField(max_length=1000)
    tinhtrang = models.BooleanField(default=True)
    ngaydat = models.DateField(default=datetime.datetime.now,null=True)

    def get_dongia(self):
        return  "%.0f" %(self.dongia)

    def get_hinhanh(self):
        return self.hinhanh
    
class DanhGia(models.Model):
    sanpham = models.ForeignKey(SanPham, on_delete=models.CASCADE,default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    noidung = models.CharField(max_length=2000,null=True)
    ngaydat = models.DateField(default=datetime.datetime.now,null=True)


class Rating(models.Model):
    sanpham = models.ForeignKey(SanPham, on_delete=models.CASCADE,default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    rating = models.IntegerField(default=0)