from itertools import count
from django.shortcuts import render
from django.db.models.query import QuerySet
from .models import *
# Create your views here.
def home(request):
    list_new_sp = SanPham.objects.all().order_by('-ngaydat')[:8]
    list_brand = Hang.objects.all()
    return render(request,'store/home.html',{'list_new_sp':list_new_sp,'list_brand':list_brand})

def shop_page(request):
    list_sp = SanPham.objects.all()
    return render(request,'store/shop.html',{'list_sp':list_sp})

def detail_product(request,id):
    sp = SanPham.objects.filter(pk=id).first()
    danhgia = DanhGia.objects.filter(sanpham=sp)[:3]

    if sp:
        return render(request,'store/detail-product.html',{'sanpham': sp,'danhgia':danhgia})

    

def list_branch(request, id):
    list_sp = SanPham.objects.filter(hang=id)
    return render(request,'store/shop.html',{'list_sp':list_sp})

def list_branch_product(request, id):
    list_sp = SanPham.objects.filter(hang=id)

    list_category = LoaiSanPham.objects.all()
    list_branch = list(Hang.objects.all())
    dem = []
    for i in list_branch:
        sp = SanPham.objects.filter(hang=i).count()
        # print(sp)
        obj = {
            'id_hang': i.id_hang,
            'tenhang': i.tenhang,
            'dem' : sp
        }
        dem.append(obj)
    # print(dem)
    # dem : chua hang va dem tung loai san pham
    return render(request,'store/category_product.html',{'list_category':list_category,'list_branch':dem,'list_sp':list_sp})

def list_category(request, id):
    list_category = LoaiSanPham.objects.filter(pk=id).first()
    # print(list_category)
    list_sp = SanPham.objects.filter(loaisanpham=list_category)
    return render(request,'store/shop.html',{'list_sp':list_sp})

def list_category_product(request, id):
    list_category = LoaiSanPham.objects.filter(pk=id).first()
    # print(list_category)
    list_sp = SanPham.objects.filter(loaisanpham=list_category)

    list_category = LoaiSanPham.objects.all()
    list_branch = list(Hang.objects.all())
    dem = []
    for i in list_branch:
        sp = SanPham.objects.filter(hang=i).count()
        # print(sp)
        obj = {
            'id_hang': i.id_hang,
            'tenhang': i.tenhang,
            'dem' : sp
        }
        dem.append(obj)
    # print(dem)
    # dem : chua hang va dem tung loai san pham
    return render(request,'store/category_product.html',{'list_category':list_category,'list_branch':dem,'list_sp':list_sp})

def category(request):
    list_category = LoaiSanPham.objects.all()
    list_branch = list(Hang.objects.all())
    dem = []
    for i in list_branch:
        sp = SanPham.objects.filter(hang=i).count()
        # print(sp)
        obj = {
            'id_hang': i.id_hang,
            'tenhang': i.tenhang,
            'dem' : sp
        }
        dem.append(obj)
    # print(dem)
    # dem : chua hang va dem tung loai san pham
    return render(request,'store/category.html',{'list_category':list_category,'list_branch':dem})

def add_review(request,id):
    sp = SanPham.objects.filter(pk=id).first()
    user = User.objects.filter(pk=request.session['id_user']).first()
    if request.method == "POST":
        print(1)

        noidung = request.POST.get('review')
        print(noidung)
        print(2)

        ngaydat = datetime.datetime.now()
        DanhGia.objects.create(sanpham = sp, user = user, noidung = noidung,ngaydat=ngaydat).save()
        return detail_product(request,id)
    else:
        return detail_product(request,id)
