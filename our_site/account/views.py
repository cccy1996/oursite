from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction as database_transaction

def account_index(request):
    return render(request, 'account/index.html')
 
def commuser_register(request):
    if request.method == 'GET':
        return render(request, 'account/commuser_register.html', {'password_err': False, 'username_err': False})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_comfirm = request.POST['password_comfirm']
        email = request.POST['email']
        
        try:
            search_user = User.objects.get(username = username)
        except Exception:
            if password != password_comfirm:
                return render(request, 'account/commuser_register.html', {'password_err': True, 'username_err': False})
            
            with database_transaction.atomic():
                new_user = User.objects.create_user(username, email = email, password = password)
                new_user.user_permissions.add('account.commuser_permission')
                new_user.save()
                relation = Commuser_relation(user = new_user, credit = 0)
                relation.save()
                login(request, new_user)
                return redirect('/account/profile/')
        return render(request, 'account/commuser_register.html', {'password_err': False, 'username_err' : True})
        #need a username duplicate check

def commuser_login(request):
    if request.method  == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return render(request, 'account/commuser_login.html', {'relog' : False})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('/account/profile/')
        else:
            return render(request, 'account/commuser_login.html', {'relog' : True})

@login_required(login_url = '/account/login/')
def commuser_profile(request):
    if request.user.has_perm('account.commuser_permission'):
        commuser = request.user.commuser_relation
        return render(request, 'account/commuser_profile.html', {'commuser' : commuser})
    elif request.user.has_perm('account.expert_permission'):
        expert = request.user.expertuser_relation
        return render(request, 'account/expert_profile.html',
                    {'isexpert': True, 'expert': expert})
    else:
        return HttpResponse("error page")

#this is a common way for both commuser and expert
def user_logout(request):
    logout(request)
    return redirect('/account')

def uesr_change_password(request):
    if request.method == 'GET':
        return render(request, 'account/change_password.html', { 'old_password_err' : False, 'new_password_err' : False})
    elif request.method == 'POST':
        username = request.POST['username']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        new_passwod_comfirm = request.POST['new_password_comfirm']

        user = authenticate(request, username = username, password = old_password)
        if user is not None:
            if (new_password == new_passwod_comfirm):
                user.set_password(new_password)
                user.save()
                return redirect('/account/logout')
            else:
                return render(request, 'account/change_password.html', { 'old_password_err' : False, 'new_password_err' : True})
        else:
            return render(request, 'account/change_password.html', { 'old_password_err' : True, 'new_password_err' : False})

def expert_register(request):
    if request.method == 'GET':
        return render(request, "account/expert_register.html", 
                        {'password_err': False, 'username_err': False, 'identity_err': False})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        email = request.POST['email']
        truename = request.POST['truename']
        identity = request.POST['identity']
    if password != password_confirm:
        return render(request, 'account/expert_register.html', 
                        {'password_err': True, 'username_err': False, 'identity_err': False})
    got = User.objects.filter(username=username)
    if (got.count() != 0):
        return render(request, 'account/expert_register.html', 
                        {'password_err': False, 'username_err': True, 'identity_err': False})
    got = Expertuser_relation.objects.filter(user__username=truename)
    if (got.count() != 0):
        return render(request, 'account/expert_register.html', 
                        {'password_err': False, 'username_err': False, 'identity_err': True})
    with database_transaction.atomic():
        new_user = User.objects.create_user(username, email = email, password = password)
        new_user.user_permissions.add('account.expert_permission')
        new_user.save()
        expert_profile = Expertuser_relation(user = new_user, name = truename, identity = identity)
        expert_profile.save()
        return redirect('/account/profile/')
                
def expert_claim_homepage(request, homepagepk):
    pass