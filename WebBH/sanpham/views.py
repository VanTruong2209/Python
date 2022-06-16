from itertools import count
import math
from django.shortcuts import redirect, render
from .models import *
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    list_new_sp = SanPham.objects.all().order_by('-ngaydat')[:8]
    list_brand = Hang.objects.all()
    return render(request,'store/home.html',{'list_new_sp':list_new_sp,'list_brand':list_brand})

def shop_page(request):
    list_sp = SanPham.objects.all()
    # mỗi trang 8sp
    paginator = Paginator(list_sp, 8)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # return render(request, 'list.html', {'page_obj': page_obj})
    return render(request,'store/shop.html',{'list_sp':page_obj})

def detail_product(request,id):
    sp = SanPham.objects.filter(pk=id).first()
    danhgia = DanhGia.objects.filter(sanpham=sp)[:3]

    #list rating chung
    rating = list(Rating.objects.filter(sanpham=sp))
    if len(rating) !=0 :
        avg_rating = 0
        for i in rating:
            avg_rating += i.rating 
        avg_rating /= len(rating)
    else:
        avg_rating = 0
    avg_rating = round(avg_rating,1)
    #list_rating_user
    try:
        user = User.objects.filter(pk=request.session['id_user']).first()
        sp = SanPham.objects.filter(pk=id).first()
        obj_rating = Rating.objects.filter(user=user,sanpham = sp).first()
        
        if obj_rating:
            rating_user = obj_rating.rating
        else: 
            rating_user = 0
    except:
        rating_user = 0
    print(rating_user)
    if sp:
        return render(request,'store/detail-product.html',{'sanpham': sp,'danhgia':danhgia,'rating':avg_rating , 'rating_user': rating_user})

    

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
    paginator = Paginator(list_sp, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # dem : chua hang va dem tung loai san pham
    return render(request,'store/category_product.html',{'list_category':list_category,'list_branch':dem,'list_sp':page_obj})

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
    paginator = Paginator(list_sp, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # dem : chua hang va dem tung loai san pham
    return render(request,'store/category_product.html',{'list_category':list_category,'list_branch':dem,'list_sp':page_obj})

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

def search(request):
    noidung = str(request.POST.get('noidung')).lower()
    list_sp = SanPham.objects.all()
    list_sp = list(list_sp)
    list_name =[]
    list_sp_result=[]
    for i in list_sp:
        list_name.append([i.tensanpham.lower(),i])
    for i in list_name: 
        if noidung in i[0]:
            list_sp_result.append(i[1])
    print(list_sp_result)
    paginator = Paginator(list_sp_result, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'store/shop.html',{'list_sp':page_obj})

def vote_rating(request,id_sp):
    try:
        user = User.objects.filter(pk=request.session['id_user']).first()
        sp = SanPham.objects.filter(pk=id_sp).first()
        obj_rating = Rating.objects.filter(user=user,sanpham = sp).first()
        vote = 0
        if '1' in request.POST:
            vote = 1
        elif '2' in request.POST:
            vote = 2
        elif '3' in request.POST:
            vote = 3
        elif '4' in request.POST:
            vote = 4
        elif '5' in request.POST:
            vote = 5
   
        if obj_rating:
            obj_rating.rating = vote
            obj_rating.save()
        else:
            Rating.objects.create(user = user, sanpham = sp , rating = vote).save()
            
        return detail_product(request,id_sp)
    except:
        return redirect('../../user/login')