
from click import confirm
from django.shortcuts import redirect, render
from .models import User
# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username, password = password)
            request.session['id_user'] = user.id_user
            request.session['hoten'] = user.hoten

            # return render(request,'home.html')
            return redirect('../../home/')
        except:
            return render(request,'login.html')
    return render(request,'login.html')

def logout(request):
    del request.session['id_user'] 
    del request.session['hoten'] 
    return redirect('../../home')
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
                User.objects.create(id_user=id_new,username=username,password=password,email=email,hoten=hoten).save()
                return login(request)

    return render(request,'register.html')