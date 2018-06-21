from django.urls import path
from . import views
app_name = 'display'

urlpatterns = [
    path('expert_detail/<int:id>',views.expert_detail,name='expert_detail'),
    path('paper_detail/<slug:id>/',views.paper_detail,name='paper_detail')
]
