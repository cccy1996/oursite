from django.urls import path
from . import views
app_name = 'display'

urlpatterns = [
    path('<int:epk>/', views.display_index, name = 'index'),
    path('show_composition_list/<int:epk>', views.show_composition_list, name = 'show_composition_list'),
    path('composition_detail/<int:epk>/<int:pk>/', views.composition_detail, name='composition_detail'),
]