from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction as database_transaction
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from django.utils import timezone
from display.models import ExpertDetail

'''
def display_index(request):
    return render(request, 'display/index.html')

def display_project(request):
    return render(request, 'display/project.html')

def display_paper(request):
    return render(request, 'display/paper.html')

def display_patent(request):
    return render(request, 'display/patent.html')

def display_detail(request):
    return render(request, 'display/detail.html')

def display_membership(request):
    return render(request, 'display/membership.html')
'''
