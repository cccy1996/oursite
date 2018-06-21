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
import json
from message.models import Inbox

def send_message(sender, to, content):
    Inbox.objects.create(inbox_date=timezone.now(), inbox_sender=sender, 
                         inbox_reciever=to, inbox_content=content)

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
                jsondict = {'login_err': True, 'perm_err': False}                
                return HttpResponse(json.dumps(jsondict), content_type="application/json")

            try:
                servant = user.customerservice
            except CustomerService.DoesNotExist:                
                jsondict = {'login_err': False, 'perm_err': True}
                return HttpResponse(json.dumps(jsondict), content_type="application/json")

            login(request, user)            
            return redirect('/customerservice/affairs/')
        else:
            assert request.method == 'GET'
            return render(request, 'customerservice/login.html')



# assume is loged in and is admin
def affairs(request):
    if not request.user.is_authenticated:
        return redirect("/customerservice/login/")
    if not request.user.has_perm('account.service_permission'):        
        raise Http404('Permission denied')

    hptodos = ApplicationForHomepageClaiming.objects.filter(state='S')
    rntodos = ApplicationForRealNameCertification.objects.filter(state='S')
    jsondict = {'homepage_claimings':[], 'realname_certifications':[]}
    for e in hptodos:
        objdict = {
            'pk': e.pk,
            'expert_account_pk': e.expert.user.pk, # Expert_relation对应的User的主键
            'homepage_pk': e.homepage.pk,
            'date': e.date,            
        }
        jsondict['homepage_claimings'].append(objdict)

    for e in rntodos:
        objdict = {
            'pk': e.pk,
            'user_pk': e.user.pk,
            'name': e.name,
            'identity': e.identity,
            'pic_url': e.pic.url,            
        }
        jsondict['realname_certifications'].append(objdict)

    return HttpResponse(json.dumps(jsondict), content_type='application/json')
    

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
        send_message(request.user, expert.user, '尊敬的用户：您的主页认领申请已经通过！赶快查看吧！')
    return redirect("/customerservice/affairs/")

def homepageclaiming_reject(request, appid):
    if request.method == "POST":
        with database_transaction.atomic():
            app = ApplicationForHomepageClaiming.objects.get(pk=appid)
            app.state = 'R'
            reason = request.POST['reason']
            app.reject_reason = reason
            app.save()
            send_message(request.user, app.expert.user, 
                    '尊敬的用户：您的主页认领申请被拒绝，理由是：{0}'.format(reason))
        return redirect("/customerservice/affairs/")
    else:
        raise Http404('')
        # return HttpResponse("How could you get here?")

def realnamecertification_accept(request, appid):
    with database_transaction.atomic():
        app = ApplicationForRealNameCertification.objects.get(pk=appid)
        user = app.user

        if user.has_perm('account.expert_permission'):            
            add_permission(user, 'verified_expert_permission')
        elif user.has_perm('account.commuser_permission'):            
            add_permission(user, 'verified_commuser_permission')
        else:
            assert False
            # return HttpResponse("fuck who you are?????????")
        user.save()
        realname_info = RealNameInfo()
        realname_info.user = user
        realname_info.name = app.name
        realname_info.identity = app.identity
        realname_info.save()
        app.state = 'P'
        app.save()
        send_message(request.user, expert.user, '尊敬的用户：您的实名认证申请已经通过！赶快查看吧！')
    return redirect("/customerservice/affairs/")

def realnamecertification_reject(request, appid):
    if request.method == 'POST':
        app = ApplicationForRealNameCertification.objects.get(pk=appid)
        app.state = 'R'
        app.reject_reason = request.POST['reason']
        app.save()
        send_message(request.user, app.expert.user, 
                    '尊敬的用户：您的实名申请申请被拒绝，理由是：{0}'.format(app.reject_reason))
        return redirect("/customerservice/affairs/")
    else:
        msg7 = {'commuser': "How could you get here?"}
        return HttpResponse(json.dumps(msg7), content_type="application/json")
        # return HttpResponse("How could you get here?")

        



