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
    path('invite_register/<int:inviter_id>/', views.invite_register, name = 'invite_register'),
    path('expert/add_project/', views.add_project, name = 'add_project'),
    path('expert/add_paper/', views.add_paper, name = 'add_paper'),
    path('expert/add_patent/', views.add_patent, name = 'add_patent'),
    path('expert/show_composition_list/', views.show_composition_list, name = 'show_composition_list'),
    path('expert/delete_composition/<int:pk>/', views.delete_composition, name = 'delete_composition'),
    path('expert/composition_detail/<int:pk>/', views.composition_detail, name='composition_detail'),

    path('expert_register/', views.expert_register, name = 'expert_register'),
    path('expert_claim_homepage/<int:homepagepk>/', 
            views.expert_claim_homepage, name = 'expert_claim_homepage'),
    path('certificate_realname/', 
            views.certificate_realname, name = 'certificate_realname'),
]
