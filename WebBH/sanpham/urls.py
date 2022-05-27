from django.urls import path, include

from . import views
app_name = 'sanpham'
urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop_page, name='shop_page'),
    path('shop/1', views.detail_product, name='detail_product'),
]
