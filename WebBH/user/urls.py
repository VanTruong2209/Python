from unicodedata import name
from django.urls import path, include

from . import views
app_name = 'user'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/',views.signup, name = 'signup'),
    path('profile/<id>',views.update_profile ,name='profile'),
    path('profile/<id>',views.update_password ,name='password'),
    path('profile/image_upload/', views.avatarView , name = 'avatarView'),
]