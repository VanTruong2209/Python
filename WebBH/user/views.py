from django.shortcuts import render
from .models import User
# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.    get('password')
        try:
            user = User.objects.get(username = username, password = password)
            return render(request,'home.html')
        except:
            return render(request,'login.html')
    return render(request,'login.html')