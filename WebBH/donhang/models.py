import datetime

from django.db import models
from sanpham.models import SanPham
from user.models import User
# Create your models here.
class DonHang(models.Model):
    id_donhang = models.IntegerField(primary_key=True,null=False)
    sanpham = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    dongia = models.FloatField(default=0)
    soluong = models.IntegerField(default=0)
    thanhtien = models.FloatField(default=0)

class ChiTietDonHang(models.Model):
    donhang = models.ForeignKey(DonHang,on_delete=models.CASCADE)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    ngaydat = models.DateField(default=datetime.datetime.now)
    hoten = models.CharField(max_length=100)
    dienthoai = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    diachinhan = models.CharField(max_length=100)
    ghichu = models.CharField(max_length=1000)
    trangthai = models.BooleanField(default=False)