from django.urls import path, include
from . import views

appname = 'customerservice'

urlpatterns = [
    path('login/', views.cs_login, name='login'),
    path('affairs/', views.affairs, name='affairs'),
    path('homepageclaiming/<int:appid>/accept/', views.homepageclaiming_accept,
         name='homepageclaiming_accept'),
    path('homepageclaiming/<int:appid>/reject/', views.homepageclaiming_reject,
         name='homepageclaiming_reject'),
    path('realnamecertification/<int:appid>/accept/', views.realnamecertification_accept,
         name='realnamecertification_accept'),
    path('realnamecertification/<int:appid>/reject/', views.realnamecertification_reject,
         name='realnamecertification_reject'),
]