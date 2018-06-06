from django.urls import path, include
from . import views

appname = 'customerservice'

urlpatterns = [
    path('register/', views.cs_register, name='register'),
    path('login/', views.cs_login, name='login'),
    path('affairs/', views.affairs, name='affairs'),
    path('homepageclaiming/<int:appid>/accept/', views.homepageclaiming_accept,
         name='homepageclaiming_accept'),
    path('homepageclaiming/<int:appid>/reject/', views.homepageclaiming_reject,
         name='homepageclaiming_reject'),
]