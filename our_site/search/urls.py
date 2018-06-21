from django.urls import path
from . import views 

app_name = 'search'

urlpatterns = [
    path('', views.search, name = 'search'),
    path('search_list/', views.search_list, name = 'search_list'),
    path('heat_analysis/', views.heat_analysis, name = 'heat_analysis'),
    
]