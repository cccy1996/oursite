from django.shortcuts import render
# Create your views here.
from account.models import Commuser_relation
from django.contrib.auth import get_user_model


def message_index(request):
    return render(request, 'message/index.html')