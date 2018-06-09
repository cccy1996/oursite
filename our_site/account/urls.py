from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.account_index, name = 'index'),
    path('login/', views.commuser_login, name = 'login'),
    path('register/', views.commuser_register, name = 'register'),
    path('profile/', views.commuser_profile, name = 'profile'),
    path('logout/', views.user_logout, name = 'logout'),
    path('changepasswd/', views.user_change_password, name = 'change_password'),

    path('expert_register/', views.expert_register, name = 'expert_register'),
    path('expert_claim_homepage/<int:homepagepk>/', 
            views.expert_claim_homepage, name = 'expert_claim_homepage'),
    path('certificate_realname/', 
            views.certificate_realname, name = 'certificate_realname'),
]
