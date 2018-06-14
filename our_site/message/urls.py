from django.urls import path
from . import views


app_name = 'message'
urlpatterns = [
    path('', views.message_index, name='index'),
    path('send', views.send_message, name='send'),
    path('read', views.read_message, name='read'),
]