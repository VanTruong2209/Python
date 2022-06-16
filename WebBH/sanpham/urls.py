from django.urls import path

from . import views
app_name = 'sanpham'
urlpatterns = [
    path('', views.home, name='home'),
    path('branch/<id>', views.list_branch, name='list_branch'),
    path('branch/<id>/product', views.list_branch_product, name='list_branch_product'),
    path('shop/', views.shop_page, name='shop_page'),
    path('shop/search', views.search, name='search'),
    
    
    path('shop/<id>', views.detail_product, name='detail_product'),
    path('shop/<id>/review', views.add_review, name='add_review'),
    path('shop/<id_sp>/vote', views.vote_rating, name='vote_rating'),


    path('category/', views.category, name='category'),
    path('category/<id>', views.list_category, name='list_category'),
    
    path('category/<id>/product', views.list_category_product, name='list_category_product'),

]
