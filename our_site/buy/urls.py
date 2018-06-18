from django.urls import path
from . import views 

app_name = 'buy'
'''
urlpatterns = [
    path('<int:pk>/', views.trans_info, name = 'trans_info'),
    path('<int:pk>/transact/', views.applicate_transact, name = 'applicate_transact'),
    path('trans_list/', views.trans_list, name = 'trans_list'),
    path('trans_list/<int:pk>/', views.bought_item, name = 'bought_item'),
    path('expert_trans_list/', views.expert_trans_list, name = 'expert_trans_list'),
    path('expert_trans_list/<int:pk>/', views.accept_trans, name = 'accept_trans'),
]
'''