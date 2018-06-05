from django.urls import path
from . import views 

app_name = 'buy'

urlpatterns = [
    path('<int:pk>/', views.transact, name='transact'),
    
]