from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.http import HttpResponse
from django.db import DatabaseError

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
        try:
            user = User.objects.create_user(username, password=password, email=email)
        except DatabaseError as e:
            return render(request, 'customerservice/register.html', 
                            {'password_err': False, 'dupusername': True})
        user.save()
        servant = CustomerService()
        servant.user = user
        servant.save()

        login(request, user)

        return redirect('/customerservice/affairs/')

# assume is loged in and is admin
def affairs(request):
    if not request.user.is_authenticated:
        return redirect("/customerservice/login/")

    todos = ApplicationForHomepageClaiming.objects.filter(state='S')
    return render(request, 'customerservice/affairs.html', {'todos': todos})

def homepageclaiming_accept(request, appid):
    app = ApplicationForHomepageClaiming.objects.get(pk=appid)
    expert = app.expert
    homepage = app.homepage
    homepage.account = expert
    homepage.save()
    expert.save()
    app.state = 'P'
    app.save()    
    return redirect("/customerservice/affairs/")

def homepageclaiming_reject(request, appid):
    if request.method == "POST":
        app = ApplicationForHomepageClaiming.objects.get(pk=appid)
        app.state = 'R'
        reason = request.POST['reason']
        app.reject_reason = reason
        app.save()
        return redirect("/customerservice/affairs/")
    else:
        return HttpResponse("How could you get here?")

        



