
from django.shortcuts import redirect, render
from pandas import period_range
from .models import *
from user.models import *
from .forms import *
import re
# Create your views here.
def view_cart(request):
    try:
        id_user = request.session['id_user']
    except:
        # print(2)
        return render(request,'store/login.html')
    user = User.objects.filter(pk = id_user).first()
    donhang_user = DonHang.objects.filter(user = user, trangthai = False).first()

    # tồn tại đơn hàng
    if donhang_user:
        list_chitiet_donhang = ChiTietDonHang.objects.filter(donhang = donhang_user)

        # total all product
        total = 0
        for i in list_chitiet_donhang:
            total+=float(i.thanhtien)

        # update tongtien of donhang
        donhang_user.tongtien = int(total)
        donhang_user.save()

        obj = {'list_chitiet_donhang' : list_chitiet_donhang,'donhang':donhang_user}
        
        request.session['id_donhang'] = donhang_user.id
        # print(1)
        return render(request,'store/cart.html',obj)
    else:
        return render(request,'store/cart.html',{})
    



def add_cart(request,id):
    try:
        id_user = request.session['id_user']
    except:
        return redirect('../../../user/login')
    sp = SanPham.objects.filter(pk=id).first()
    user = User.objects.get(pk = id_user)
    donhang_user = DonHang.objects.filter(user=user,trangthai=False).first()
    # thêm vào đơn hàng đó
    if donhang_user:
        chitiet = ChiTietDonHang.objects.filter(donhang=donhang_user,sanpham = sp).first()
        # Ktr tốn tại chi tiết thì tăng thêm số lượng
        if chitiet:
            chitiet.soluong+=1
            chitiet.save()
        else:
            ChiTietDonHang(donhang=donhang_user,sanpham=sp,soluong=1).save()
        request.session['id_donhang'] = donhang_user.id
        
    else:
        print(user)
        donhang = DonHang.objects.create(user = user)
        donhang.save()
        chitiet = ChiTietDonHang(donhang=donhang,sanpham=sp,soluong=1)
        chitiet.save()
        print(1)
        request.session['id_donhang'] = donhang.id
    return view_cart(request)
    

def update_cart(request, list_id):
    list_chitiet=[]
    list_sp=list_soluong=[]
    chuoi = str(list_id)
    id = re.findall(r'\d+', chuoi)
    id = list(map(lambda x: int(x),id))
    # print(id)
    for item in id:
        list_chitiet.append(ChiTietDonHang.objects.get(pk=item))
    for item in list_chitiet:
        list_sp.append(item.sanpham.id_sanpham)
    print(list_sp)
    # print(request.POST.get('soluong_19'))
    # for item in list_sp:
        # list_id_result.append(request.POST.get('\''+'soluong_'+str(item)+'\''))
    dem=0;
    for item in list_sp:
        chuoi='soluong_'+str(item)
        
        list_soluong[dem] = (request.POST.get(chuoi))
        dem+=1

    for i in range(0,len(id)):
        edit = ChiTietDonHang.objects.get(pk=id[i])
        edit.soluong = list_soluong[i]
        edit.save()
        print(edit.soluong)
    return redirect('../')


def remove_cart(request,id):
    id_donhang = request.session['id_donhang']
    donhang = DonHang.objects.get(pk=id_donhang)
    sp = SanPham.objects.get(pk=id)
    ChiTietDonHang.objects.filter(donhang=donhang,sanpham=sp).first().delete()
    return redirect('../')

def clear_cart(request):
    pass

def thanhtoan(request, id_donhang):
    donhang = DonHang.objects.get(pk=id_donhang)
    chitiet = ChiTietDonHang.objects.filter(donhang=donhang)
    total = 0
    for item in chitiet:
        total += float(item.thanhtien) 
    donhang.tongtien = total
    donhang.trangthai = 'True'
    donhang.save()
    return view_cart(request)