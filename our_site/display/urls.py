from django.urls import path
from . import views

app_name = 'display'

urlpatterns = [
    path('', views.display_index, name = 'index'),
    path('project/', views.display_project, name = 'project'),
    path('paper/', views.display_paper, name = 'paper'),
    path('patent/', views.display_patent, name = 'patent'),
    path('detail/', views.display_detail, name = 'detail'),
    path('membership/', views.display_membership, name = 'membership'),
]