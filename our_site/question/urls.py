from django.urls import path
from . import views

app_name = 'question'

urlpatterns = [
    path('', views.question_index, name='index'),
    path('askquestion', views.consumer_ask_question, name='ask_question'),
    path('question/<int:queid>', views.consumer_question_detail, name='question_detail'),
    path('list/<int:quetype>', views.consumer_question_list, name='question_list'),
]
