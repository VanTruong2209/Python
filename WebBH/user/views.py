
from click import confirm
from django.shortcuts import redirect, render
from .models import User
from .forms import *
# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username, password = password)
            request.session['id_user'] = user.id_user
            request.session['hoten'] = user.hoten
            request.session['quyen'] = user.quyen
            # return render(request,'home.html')
            return redirect('../../')
        except:
            return render(request,'store/login.html')
    return render(request,'store/login.html')

def logout(request):
    del request.session['id_user'] 
    del request.session['hoten'] 
    del request.session['quyen']
 
    return redirect('../../')
    # return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password= request.POST.get('password')
        email = request.POST.get('email')
        confirm = request.POST.get('confirm')
        hoten = request.POST.get('hoten')
        user = User.objects.filter(username = username).first()
        print(user)

        if user is None:
            if confirm == password:
                print(1)
                user = User.objects.all().order_by('-id_user').first()
                id_new = user.id_user+1
                User.objects.create(id_user=id_new,username=username,password=password,email=email,hoten=hoten,quyen = False).save()
                return login(request)

    return render(request,'store/register.html')

def update_profile(request,id):
    user = User.objects.filter(pk = id).first()
    if request.method == 'POST':
        email = request.POST.get('email')
        hoten = request.POST.get('hoten')
        gioitinh = request.POST.get('gioitinh')
        dienthoai = request.POST.get('dienthoai')
        diachi = request.POST.get('diachi')
   
        user_update = { 'email' : email, 'hoten':hoten, 'gioitinh' : gioitinh, 'dienthoai' : dienthoai, 'diachi': diachi}
        form = UserForm(user_update,instance=user)
        if form.is_valid():
            form.save()
        return redirect('../../')
    form = UserImageForm()
    return render(request,'store/update_profile.html',{'user':user,'form1':form})

def update_password(request,id):
    user = User.objects.filter(pk = id).first()
    form_image = UserImageForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password_cur= request.POST.get('password_cur')
        password_new= request.POST.get('password_new')
        confirm = request.POST.get('confirm')

        if confirm != password_new or password_cur != user.password: 
            print('1')
            return render(request,'store/update_profile.html',{'user':user,'form1' : form_image,'trangthai': 2})
        user_update = { 'username' : username, 'password' : password_new }

        form = UserPassForm(user_update,instance=user)
        if form.is_valid():
            form.save()
        print(2)
        return render(request,'store/update_profile.html',{'user':user,'form1' : form_image,'trangthai':1})
    # print(2)
    # return render(request,'store/update_profile.html',{'user':user,'form1' : form_image })

def avatarView(request):
    id_user = request.session['id_user']
    # print(id_user)
    if request.method == "POST":
        user = User.objects.get(pk=id_user)
        # BUG
        # Chưa add vào folder
        form = UserImageForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            print(1)
            form.save()
        return redirect('../../../')
    