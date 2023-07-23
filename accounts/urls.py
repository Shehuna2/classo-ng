from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('about/', views.aboutUs, name='about-us'),
    path('profile/', views.userProfile, name='profile'),
]