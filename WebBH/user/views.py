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
    pass