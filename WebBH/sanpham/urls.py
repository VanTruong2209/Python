from django.urls import path, include

from . import views
app_name = 'sanpham'
urlpatterns = [
    path('', views.home, name='home'),
]
