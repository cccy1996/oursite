from django.urls import path
from . import views

app_name = 'question'

urlpatterns = [
    path('', views.question_index, name='index'),
    path('ask_question', views.consumer_ask_question, name='ask_question'),
    path('question/<int:queid>', views.question_detail, name='question_detail'),
    path('list/<int:quetype>', views.question_list, name='question_list'),
    path('answer_question/<int:queid>', views.expert_answer_question, name='answer_question'),
]
