

# Create your models here.
from re import A
from django.db import models
import datetime
from django.db import models
from sanpham.models import SanPham
from user.models import User
# Create your models here.

class DonHang(models.Model):
    # donhang = models.ForeignKey(DonHang,on_delete=models.CASCADE)
    # id_donhang = models.IntegerField(primary_key=True,null=False)
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    ngaydat = models.DateField(default=datetime.datetime.now)
    hoten = models.CharField(max_length=100,blank=True,default='')
    dienthoai = models.CharField(max_length=100,blank=True,default='')
    # email = models.EmailField(max_length=100,null=True)
    diachinhan = models.CharField(max_length=100,blank=True,default='')
    ghichu = models.CharField(max_length=1000,blank=True,default='')
    trangthai = models.BooleanField(default=False)
    tongtien = models.FloatField(null=False,default=0)

class ChiTietDonHang(models.Model):
    # id_chitietdonhang = models.IntegerField(primary_key=True,null=False)
    id = models.AutoField(primary_key=True)
    donhang = models.ForeignKey(
        DonHang,
        on_delete=models.CASCADE,
    )
    sanpham = models.ForeignKey(SanPham , on_delete=models.CASCADE)
    dongia = models.FloatField(default=0)
    soluong = models.IntegerField(default=0)
    # thanhtien = models.FloatField(default=0)

    @property
    def thanhtien(self):
        return "%.0f" %(self.soluong * float(self.sanpham.get_dongia()))