from django.shortcuts import render
from .models import *
# Create your views here.
def home(request):
    list_new_sp = SanPham.objects.all()[:6]
    # print(list_new_sp)
    list_brand = Hang.objects.all()
    return render(request,'home.html',{'list_new_sp':list_new_sp,'list_brand':list_brand})

def shop_page(request):
    list_sp = SanPham.objects.all()
    return render(request,'shop.html',{'list_sp':list_sp})

def detail_product(request):
    sp = SanPham.objects.filter(pk=1).first()
    if sp:
        return render(request,'detail-product.html',{'sanpham': sp})