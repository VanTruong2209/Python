from django.urls import path

from . import views
app_name = 'donhangs'
urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<id>', views.add_cart, name='add_cart'),
    path('update/<list_id>', views.update_cart, name='update_cart'),
    path('remove/<id>', views.remove_cart, name='remove_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('thanhtoan/<id_donhang>',views.thanhtoan,name = 'thanhtoan')
]
