from django.urls import path
from . import views
app_name = 'display'
'''
urlpatterns = [
<<<<<<< HEAD
    path('', views.display_index, name = 'index'),
    path('project/', views.display_project, name = 'project'),
    path('paper/', views.display_paper, name = 'paper'),
    path('patent/', views.display_patent, name = 'patent'),
    path('detail/', views.display_detail, name = 'detail'),
    path('membership/', views.display_membership, name = 'membership'),
]
'''


=======
    path('<int:epk>/', views.display_index, name = 'index'),
    path('show_composition_list/<int:epk>', views.show_composition_list, name = 'show_composition_list'),
    path('composition_detail/<int:epk>/<int:pk>/', views.composition_detail, name='composition_detail'),
]
>>>>>>> c5c17c47fa891cac7c7c1bbb6e28289fe7d5471a
