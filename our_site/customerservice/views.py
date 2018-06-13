from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from .models import *
from django.http import HttpResponse
from django.db import DatabaseError
from django.db import transaction as database_transaction
from account.models import User_Permission, RealNameInfo, Expertuser_relation

def add_permission(user, permstr):
    content_type = ContentType.objects.get_for_model(User_Permission)
    permission = Permission.objects.get(content_type = content_type, codename = permstr)
    user.save()
    user.user_permissions.add(permission)       

def cs_login(request):
    if request.user.is_authenticated:
        return redirect('/customservice/affairs/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']            
            user = authenticate(request, username=username, password=password)
            if user is None:
                return HttpResponse("username or password error")

            try:
                servant = user.customerservice
            except CustomerService.DoesNotExist:
                return HttpResponse("the user name exists, but you are not a admin")

            login(request, user)            
            return redirect('/customerservice/affairs/')
        else:
            assert request.method == 'GET'
            return render(request, 'customerservice/login.html')

def cs_register(request):
    if request.method == 'GET':
        return render(request, 'customerservice/register.html', 
                        {'password_err': False, 'dupusername': False})
    else:
        assert request.method == 'POST'        
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        if password != password_confirm:
            return render(request, 'customservice/register.html', 
                            {'password_err': True, 'dupusername': False})
        email = request.POST['email']
        with database_transaction.atomic():
            try:
                user = User.objects.create_user(username, password=password, email=email)
            except DatabaseError as e:
                return render(request, 'customerservice/register.html', 
                                {'password_err': False, 'dupusername': True})
            add_permission(user, 'service_permission')
            servant = CustomerService()
            servant.user = user
            servant.save()

        login(request, user)

        return redirect('/customerservice/affairs/')

# assume is loged in and is admin
def affairs(request):
    if not request.user.is_authenticated:
        return redirect("/customerservice/login/")
    if not request.user.has_perm('account.service_permission'):
        return HttpResponse("You don't have admin permission!!!")

    hptodos = ApplicationForHomepageClaiming.objects.filter(state='S')
    rntodos = ApplicationForRealNameCertification.objects.filter(state='S')
    return render(request, 'customerservice/affairs.html', 
                        {'hptodos': hptodos, 'rntodos': rntodos})

#TODO: 怎样通知相关用户其申请是否通过？

def homepageclaiming_accept(request, appid):
    with database_transaction.atomic():
        app = ApplicationForHomepageClaiming.objects.get(pk=appid)
        expert = app.expert
        expert.save()
        homepage = app.homepage
        homepage.account = expert
        homepage.save()        
        app.state = 'P'
        app.save()
    return redirect("/customerservice/affairs/")

def homepageclaiming_reject(request, appid):
    if request.method == "POST":
        with database_transaction.atomic():
            app = ApplicationForHomepageClaiming.objects.get(pk=appid)
            app.state = 'R'
            reason = request.POST['reason']
            app.reject_reason = reason
            app.save()
        return redirect("/customerservice/affairs/")
    else:
        return HttpResponse("How could you get here?")

def realnamecertification_accept(request, appid):
    with database_transaction.atomic():
        app = ApplicationForRealNameCertification.objects.get(pk=appid)
        user = app.user
        if user.has_perm('account.expert_permission'):            
            add_permission(user, 'verified_expert_permission')
        elif user.has_perm('account.commuser_permission'):            
            add_permission(user, 'verified_commuser_permission')
        else:
            return HttpResponse("fuck who you are?????????")
        user.save()
        realname_info = RealNameInfo()
        realname_info.user = user
        realname_info.name = app.name
        realname_info.identity = app.identity
        realname_info.save()
        app.state = 'P'
        app.save()
    return redirect("/customerservice/affairs/")

def realnamecertification_reject(request, appid):
    if request.method == 'POST':
        app = ApplicationForRealNameCertification.objects.get(pk=appid)
        app.state = 'R'
        app.reject_reason = request.POST['reason']
        app.save()
        return redirect("/customerservice/affairs/")
    else:
        return HttpResponse("How could you get here?")

        



