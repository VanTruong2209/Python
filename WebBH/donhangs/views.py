
from django.shortcuts import redirect, render
from numpy import char
from .models import *
from user.models import *
from .forms import *
import re
import calendar
from datetime import datetime
from django.db.models import Q
from collections import OrderedDict
from datetime import date
from sanpham.models import LoaiSanPham
# Include the `fusioncharts.py` file that contains functions to embed the charts.
from .fusioncharts import FusionCharts
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
    if sp.soluong <= 0:
        return render(request,'store/outofproduct.html')
    
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
        donhang = DonHang.objects.create(user = user)
        donhang.save()
        chitiet = ChiTietDonHang(donhang=donhang,sanpham=sp,soluong=1)
        chitiet.save()

        request.session['id_donhang'] = donhang.id
    
    # soluong sanpham giam
    sp.soluong -= 1
    sp.save()
    return view_cart(request)
    
def add_cart_num(request,id):
    try:
        id_user = request.session['id_user']
    except:
        return redirect('../../../user/login')
    sp = SanPham.objects.filter(pk=id).first()
    
    if sp.soluong < int(request.POST.get('soluong')):
        return render(request,'store/outofproduct.html',{"sl_conlai": sp.soluong})
    
    user = User.objects.get(pk = id_user)
    donhang_user = DonHang.objects.filter(user=user,trangthai=False).first()
    # thêm vào đơn hàng đó
    if donhang_user:
        chitiet = ChiTietDonHang.objects.filter(donhang=donhang_user,sanpham = sp).first()
        # Ktr tốn tại chi tiết thì tăng thêm số lượng
        if chitiet:
            chitiet.soluong+=int(request.POST.get('soluong'))
            chitiet.save()
        else:
            ChiTietDonHang(donhang=donhang_user,sanpham=sp,soluong=int(request.POST.get('soluong'))).save()
        request.session['id_donhang'] = donhang_user.id
        
    else:

        donhang = DonHang.objects.create(user = user)
        donhang.save()
        chitiet = ChiTietDonHang(donhang=donhang,sanpham=sp,soluong=int(request.POST.get('soluong')))
        chitiet.save()
        request.session['id_donhang'] = donhang.id
        
    sp.soluong -= int(request.POST.get('soluong'))
    sp.save()    
    return view_cart(request)


def update_cart(request, list_id):
    list_chitiet=[]
    list_sl_tontai=[]
    list_soluong_moi=[]
    list_sl_cu=[]
   
    chuoi = str(list_id)
    id = re.findall(r'\d+', chuoi)
    id = list(map(lambda x: int(x),id))

    for item in id:
        list_chitiet.append(ChiTietDonHang.objects.filter(pk=item).first())
    # print(list_chitiet)
    list_sp=[]
    for i in range(0,len(list_chitiet)):
        list_sp.append(list_chitiet[i].sanpham.id_sanpham)
        list_sl_tontai.append(list_chitiet[i].sanpham.soluong)
        list_sl_cu.append(list_chitiet[i].soluong)

    for item in list_sp:
        chuoi='soluong_'+str(item)  
        list_soluong_moi.append(request.POST.get(chuoi))
    
    list_check=[]
    for i in range(0,len(list_sl_tontai)):
        if  int(list_sl_tontai[i]) >= (int(list_soluong_moi[i]) - int(list_sl_cu[i])):
            list_check.append(True)
        else:
            list_check.append(False)
            
    list_sp_outof =[]
    for i in range(0,len(id)):
        edit = ChiTietDonHang.objects.get(pk=id[i])
        sp = SanPham.objects.filter(pk=edit.sanpham.id_sanpham).first()
        if list_check[i]:
            edit.soluong = list_soluong_moi[i]
            edit.save()
            sp.soluong -= (int(list_soluong_moi[i]) - int(list_sl_cu[i]))
            sp.save()
        else:
            list_sp_outof.append({'sp':sp,'sl':list_soluong_moi[i]})
    print(list_check)
    if all(list_check):
        return redirect('../')
    else: 
        return render(request,'store/outofproduct.html',{"list_sp_outof":list_sp_outof})

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

def history(request):
    id = request.session['id_user']
    user = User.objects.get(pk=id)
    donhang = DonHang.objects.filter(user=user).order_by('trangthai')
    return render(request,'store/history.html',{'listorder':donhang})

def chitiet(request,id):
    donhang = DonHang.objects.filter(id= id).first()
    list = ChiTietDonHang.objects.filter(donhang=donhang)
    return render(request,'store/listDetail.html',{'list':list})

def bieudodoanhthu(month,year):
    d_fmt = "{0:>02}.{1:>02}.{2}"
    date_from = datetime.strptime(d_fmt.format(1, month, year), '%d.%m.%Y').date()
    last_day_of_month = calendar.monthrange(year, month)[1]
    date_to = datetime.strptime(d_fmt.format(last_day_of_month, month, year), '%d.%m.%Y').date()

    list_ct = ChiTietDonHang.objects.filter(Q(donhang__ngaydat__gte=date_from, donhang__ngaydat__lte=date_to)|Q(donhang__ngaydat__lt=date_from, donhang__ngaydat__gte=date_from))
    list_ct = list(list_ct)
    list_ct_edit = []
    list_id=[]
    for i in list_ct:
        list_id.append(i.sanpham.id_sanpham)
        list_ct_edit.append([i.sanpham,i.soluong])
    map_id = list(set(list_id))  # mảng chưa id 
    list_sl = []                # mảng chứa sl đã bán 
    for id in map_id:
        sl = 0
        for i in list_ct_edit:
            if id == i[0].id_sanpham:
                sl += i[1]
        list_sl.append(sl)
    list_sp = list(map(lambda x,y: {"sanpham" : SanPham.objects.get(pk=x), "soluongban": y}, map_id ,list_sl))
    for i in list_sp:
        i["doanhthu"] = i["sanpham"].dongia * i["soluongban"]
    doanthu = 0
    for i in list_sp:
        doanthu += i["doanhthu"]
    return  {"doanhthu" : doanthu ,  "list_sp" : list_sp}


def chart_month(thang , doanhthuthang , ten_x , ten_y , tenbd):
    dataSource = OrderedDict()
    dataSource["data"] = []
    for i in range(0,len(thang)):
        if i == 0 and thang[0] == 0:
            continue
        dataSource["data"].append({"label": str(thang[i]), "value": doanhthuthang[i]})

    chartConfig = OrderedDict()
    chartConfig["caption"] = tenbd
    chartConfig["xAxisName"] = ten_x
    chartConfig["yAxisName"] = ten_y
    chartConfig["numberSuffix"] = ""
    chartConfig["theme"] = "fusion"

    dataSource["chart"] = chartConfig
    column2D = FusionCharts("column2d", "myFirstChart", "600", "300", "myFirstchart-container", "json", dataSource)
    return column2D
    
def doanhthu(request):
    if request.method == "POST":
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        obj = bieudodoanhthu(month,year) 
        [tron, cot] = doanhthu_catelogy(month,year)
        return render(request,"store/doanhthu.html",{"list_sp":obj['list_sp'],"doanhthu" : obj['doanhthu'], 'output_tron' : tron.render(), 'output_cot' : cot.render() , 'month':month, 'year':year })
        # return render(request,"store/doanhthu.html",{"list_sp":obj['list_sp'],"doanhthu" : obj['doanhthu']})
    else:
        thang = []
        doanhthu_ = []
        thang.append(0)
        doanhthu_.append(0)       
        for i in range(1,date.today().month+1):
            doanhthu_.append(bieudodoanhthu(i,2022)['doanhthu'])
            thang.append(i)
        column2D =  chart_month(thang,doanhthu_,"tháng","Doanh thu (VNĐ)","Doanh thu theo tháng năm 2022")
        # [tron, cot] = doanhthu_catelogy(6,2022)
        return render(request,"store/doanhthu.html",{'output' : column2D.render()})
        # obj = bieudodoanhthu(month,year) 
        # return render(request,"store/doanhthu.html",{"list_sp":obj['list_sp'],"doanhthu" : obj['doanhthu']})
    
def doanhthu_catelogy(month,year):
    d_fmt = "{0:>02}.{1:>02}.{2}"
    date_from = datetime.strptime(d_fmt.format(1, month, year), '%d.%m.%Y').date()
    last_day_of_month = calendar.monthrange(year, month)[1]
    date_to = datetime.strptime(d_fmt.format(last_day_of_month, month, year), '%d.%m.%Y').date()

    list_ct = ChiTietDonHang.objects.filter(Q(donhang__ngaydat__gte=date_from, donhang__ngaydat__lte=date_to)|Q(donhang__ngaydat__lt=date_from, donhang__ngaydat__gte=date_from))
    list_ct = list(list_ct)
    list_ct_edit = []
    list_id=[]
    list_cate=[]
    for i in list_ct:
        list_id.append(i.sanpham.id_sanpham)
        list_ct_edit.append([i.sanpham,i.soluong])
        list_cate.append(i.sanpham.loaisanpham.id_loaisanpham)
    map_id = list(set(list_cate))  # mảng chưa id 
    list_sl = []                # mảng chứa sl đã bán 
    for id in map_id:
        sl = 0
        for i in list_ct_edit:
            if id == i[0].loaisanpham.id_loaisanpham:
                sl += i[1]*i[0].dongia
        list_sl.append(sl)
    list_sp = list(map(lambda x,y: {"loaisanpham" : LoaiSanPham.objects.get(pk=x), "doanhthu": y}, map_id ,list_sl))
    truc_dt=[]
    truc_sp=[]
    for i in list_sp:
        truc_dt.append(i['doanhthu'])
        truc_sp.append(i['loaisanpham'].tenloaisanpham)
    
    return [chart_tron_cate(list_sp) , chart_month(truc_sp,truc_dt,"loại sản phẩm" , "Doanh thu (VNĐ)" , "Doanh thu theo loại sp")]

def chart_tron_cate(list_cate):
    chuoi = ""
    for i in list_cate:
        chuoi += " { 'label': '" + str(i['loaisanpham'].tenloaisanpham) +"', 'value': '" + str(i['doanhthu']) + "'}, "
    chuoi1 = """{
        "chart": {
        "caption": "Doanh thu theo loại sản phẩm ",
        "plottooltext": "<b>$percentValue</b> tổng doanh thu",
        "showlegend": "1",
        "showpercentvalues": "1",
        "legendposition": "bottom",
        "usedataplotcolorforlabels": "1",
        "theme": "fusion"
        },
        "data": [
        """ + chuoi + """
    ]
    }"""
    print(chuoi)
    chartObj = FusionCharts( 'pie2d', 'ex1', '500', '300', 'chart-1', 'json', chuoi1)   
    return chartObj