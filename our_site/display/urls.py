from django.urls import path
from . import views

app_name = 'display'
'''
urlpatterns = [
    path('<int:epk>/', views.display_index, name = 'index'),
    path('<int:epk>/show_composition_list/', views.show_composition_list, name = 'show_composition_list'),
    path('<int:epk>/composition_detail/<int:pk>/', views.composition_detail, name='composition_detail'),
]
'''