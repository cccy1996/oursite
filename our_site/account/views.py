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
import datetime
from display.models import *
import json
from django.http import HttpResponse
from django.utils import timezone
from customerservice.models import ApplicationForHomepageClaiming, ApplicationForRealNameCertification
from .forms import *
from django.core import serializers


def account_index(request):
   return render(request, 'account/index.html')


def commuser_register(request):
    if request.method == 'GET':
        msg1 = {'password_err': False, 'username_err': False}
        return HttpResponse(json.dumps(msg1), content_type="application/json")
        # return render(request, 'account/commuser_register.html', {'password_err': False, 'username_err': False})

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_comfirm = request.POST['password_comfirm']
        email = request.POST['email']
        
        try:
            search_user = User.objects.get(username = username)
        except Exception:
            if password != password_comfirm:
                msg2 = {'password_err': True, 'username_err': False}
                return HttpResponse(json.dumps(msg2), content_type="application/json")
                # return render(request, 'account/commuser_register.html', {'password_err': True, 'username_err': False})
            
            with database_transaction.atomic():
                new_user = User.objects.create_user(username, email = email, password = password)
                
                content_type = ContentType.objects.get_for_model(User_Permission)
                permission = Permission.objects.get(content_type = content_type,codename = 'commuser_permission')
                new_user.save()
                new_user.user_permissions.add(permission)
                relation = Commuser_relation(user = new_user, credit = 0)
                relation.save()
            login(request, new_user)
            return redirect('/account/profile/')

        msg3 = {'password_err': False, 'username_err': True}
        return HttpResponse(json.dumps(msg3), content_type="application/json")
        # return render(request, 'account/commuser_register.html', {'password_err': False, 'username_err' : True})


def commuser_login(request):
    if request.method  == 'GET':
        if request.user.is_authenticated:
            #logout(request)
            return redirect('/account/profile')

        msg4 = {'relog' : False}
        return HttpResponse(json.dumps(msg4), content_type="application/json")
       # return render(request, 'account/commuser_login.html', {'relog' : False})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            #登陆时直接比较登陆时间来增加积分
            if user.has_perm('account.commuser_permission'):
                if user.last_login + datetime.timedelta(days = 1) < timezone.now():
                    user.commuser_relation.credit += 10
                    user.commuser_relation.save()
            login(request, user)
            return redirect('/account/profile/')
        else:
            msg5 = {'relog': False}
            return HttpResponse(json.dumps(msg5), content_type="application/json")
           # return render(request, 'account/commuser_login.html', {'relog' : True})

@login_required(login_url = '/account/login/')
def commuser_profile(request):
    jsondict = {
        'userpk': request.user.pk,
        'username': request.user.username,        
    }
    try:
        realnameinfo = request.user.realnameinfo
        jsondict['realname'] = realnameinfo.name
    except RealNameInfo.DoesNotExist:
        pass

    if request.user.has_perm('account.commuser_permission'):
        commuser = request.user.commuser_relation
        jsondict['isexpert'] = False
        jsondict['credit'] = commuser.credit                
    elif request.user.has_perm('account.expert_permission'):
        expert = request.user.expertuser_relation
        jsondict['isexpert'] = True
        try:
            homepage = expert.expertdetail
            jsondict['homepagepk'] = homepage.pk
        except ExpertDetail.DoesNotExist:
            pass
    else:
        assert False
    return HttpResponse(json.dumps(jsondict), content_type="application/json")

#this is a common way for both commuser and expert
def user_logout(request):
    logout(request)
    return redirect('/account')

@login_required(login_url = '/account/login/')
def user_change_password(request):
    if request.method == 'GET':
        msg9 = {'old_password_err' : False, 'new_password_err': False}
        return HttpResponse(json.dumps(msg9), content_type="application/json")
        # return render(request, 'account/change_password.html', { 'old_password_err' : False, 'new_password_err' : False})
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
                msg10 = {'old_password_err': False, 'new_password_err': False}
                return HttpResponse(json.dumps(msg10), content_type="application/json")
                # return render(request, 'account/change_password.html', { 'old_password_err' : False, 'new_password_err' : True})
        else:
            return render(request, 'account/change_password.html', { 'old_password_err' : True, 'new_password_err' : False})

def expert_register(request):
    if request.method == 'GET':
        msg11 ={'password_err': False, 'username_err': False, 'identity_err': False}
        return HttpResponse(json.dumps(msg11), content_type="application/json")
        # return render(request, "account/expert_register.html",
                        # {'password_err': False, 'username_err': False, 'identity_err': False})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        email = request.POST['email']
        truename = request.POST['truename']
        identity = request.POST['identity']
    if password != password_confirm:
        msg12 = {'password_err': True, 'username_err': False, 'identity_err': False}
        return HttpResponse(json.dumps(msg12), content_type="application/json")
        # return render(request, 'account/expert_register.html',
                        # {'password_err': True, 'username_err': False, 'identity_err': False})
    got = User.objects.filter(username=username)
    if (got.count() != 0):
        msg13 =  {'password_err': False, 'username_err': True, 'identity_err': False}
        return HttpResponse(json.dumps(msg13), content_type="application/json")
        # return render(request, 'account/expert_register.html',
                        # {'password_err': False, 'username_err': True, 'identity_err': False})
    got = Expertuser_relation.objects.filter(user__username=truename)
    if (got.count() != 0):
        msg14 = {'password_err': False, 'username_err': False, 'identity_err': True}
        return HttpResponse(json.dumps(msg14), content_type="application/json")
        # return render(request, 'account/expert_register.html',
                        # {'password_err': False, 'username_err': False, 'identity_err': True})
    with database_transaction.atomic():
        new_user = User.objects.create_user(username, email = email, password = password)
        new_user.save()
        content_type = ContentType.objects.get_for_model(User_Permission)
        permission = Permission.objects.get(content_type = content_type,codename = 'expert_permission')
        new_user.user_permissions.add(permission)
        expert_profile = Expertuser_relation(user = new_user, name = truename, identity = identity)
        expert_profile.save()
    return redirect('/account/profile/')


@login_required(login_url = '/account/login/')

def expert_claim_homepage(request, homepagepk):
    user = request.user
    expert = user.expertuser_relation
    try:
        detail = expert.expertdetail        
        jsondict = {'already_have_one_err': True, 'not_owned_err': False}
        return HttpResponse(json.dumps(jsondict), content_type="application/json")
        # return HttpResponse("you've already had a homepage")
    except ExpertDetail.DoesNotExist:
        # this is the correct branch
        try:
            wanted = ExpertDetail.objects.get(pk=homepagepk)
        except ExpertDetail.DoesNotExist:
            raise Http404('')            
        if wanted.name != expert.name:
            jsondict = {'not_owned_err': True, 'already_have_one_err': False}
            return HttpResponse(json.dumps(jsondict), content_type="application/json")
        apply = ApplicationForHomepageClaiming.objects.create(
            expert=expert, homepage=wanted, date=timezone.now(), state='S',
        )
        apply.save()

        return redirect('/account/profile/')

@login_required(login_url = '/account/login/')
def certificate_realname(request):
    user = request.user
    if user.has_perm('account.verified_expert_permission') or user.has_perm(
        'account.verified_commuser_permission'):
        jsondict = {'already_certificated': True}
        return HttpResponse(json.dumps(jsondict), content_type="application/json")
        # return HttpResponse("你已经认证过了")
    if request.method == 'GET':
        form = RealNameForm()
        msg19 = {'form': form, 'invalid': False}

        return HttpResponse(json.dumps(msg19), content_type="application/json")
        # return render(request,
                # "account/certificate_realname.html", {'form': form, 'invalid': False})
    else:
        assert request.method == 'POST'
        form = RealNameForm(request.POST, request.FILES)
        if form.is_valid():
            application = ApplicationForRealNameCertification.objects.create(
                user=user, name=request.POST['realname'], identity=request.POST['identity'],
                pic=request.FILES['pic'], state='S',
            )
            application.save()
            """ msg20 = {'msg': "application commited successfully! please wait for shenhe"}
            return HttpResponse(json.dumps(msg20), content_type="application/json") """
            return redirect('/account/profile/')
            # return HttpResponse("application commited successfully! please wait for shenhe")
        else:
            form = RealNameForm()
            msg21 = {'form': form, 'invalid': True}
            return HttpResponse(json.dumps(msg21), content_type="application/json")
            # return render(request, "account/certificate_realname.html",
                            # {'form': form, 'invalid': True})

def invite_register(request, inviter_id):
    if request.method == 'GET':
        inviter = User.objects.filter(id = inviter_id)
        if inviter.count() == 0 or inviter[0].has_perm('account.commuser_permission') == False:
            msg22 = {'msg': "邀请人不存在"}
            return HttpResponse(json.dumps(msg22), content_type="application/json")
            # return HttpResponse("邀请人不存在")
        msg23 = {'password_err': False, 'username_err': False}
        return HttpResponse(json.dumps(msg23), content_type="application/json")
        # return render(request, 'account/commuser_register.html', {'password_err': False, 'username_err': False})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_comfirm = request.POST['password_comfirm']
        email = request.POST['email']
        
        try:
            search_user = User.objects.get(username = username)
        except Exception:
            if password != password_comfirm:
                msg24 = {'password_err': True, 'username_err': False}
                return HttpResponse(json.dumps(msg24), content_type="application/json")
                # return render(request, 'account/commuser_register.html', {'password_err': True, 'username_err': False})
            inviter = User.objects.get(id = inviter_id)
            with database_transaction.atomic():
                new_user = User.objects.create_user(username, email = email, password = password)
                content_type = ContentType.objects.get_for_model(User_Permission)
                permission = Permission.objects.get(content_type = content_type,codename = 'commuser_permission')
                new_user.save()
                new_user.user_permissions.add(permission)
                relation = Commuser_relation(user = new_user, credit = 0)
                relation.save()
                inviter.commuser_relation.credit += 10
                inviter.commuser_relation.save()
            login(request, new_user)
            return redirect('/account/profile/')
        msg25 = {'password_err': False, 'username_err' : True}
        return HttpResponse(json.dumps(msg25), content_type="application/json")
        # return render(request, 'account/commuser_register.html', {'password_err': False, 'username_err' : True})
    
'''
def create_composition(request):
    composition = Composition.objects.create(
        comp_name = request.POST['comp_name'],
        upload_time = timezone.now(),
        expert = request.user.expertuser_relation,
        price = request.POST['price'],
        description = request.POST['description'],
    )
    composition.save()
    return composition

def save_appendix(request, composition):
    files = request.FILES.getlist('appendixes')
    for f in files:
        appendix = Appendix.objects.create(
            composition = composition,
            uploaded = f,
        )
        appendix.save()

def save_display_materials(request, composition):
    pics = request.FILES.getlist('pictures')
    for p in pics:
        pic = DisplayMaterial.objects.create(
            composition = composition,
            uploaded = p,
            material_type = 'P',
            description = 'a picture',
        )
        pic.save()
    videos = request.FILES.getlist('videos')
    for v in videos:
        video  = DisplayMaterial.objects.create(
            composition = composition,
            uploaded = p,
            material_type = 'V',
            description = 'a video',
        )
        video.save()



def save_uploaded(request, composition):
    save_appendix(request, composition)
    save_display_materials(request, composition)

@login_required()
#@permission_required('account.verified_expert_permission', raise_exception=True)
def add_project(request):
    if request.method == 'GET':
        form = ProjectForm()
        return render(request, 'account/add_project.html', {'form':form, 'invalid':False})
    else:
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            with database_transaction.atomic():
                composition = create_composition(request)            
                project = Project.objects.create(
                    composition = composition,
                    organization = request.POST['organization'],
                    start_time = request.POST['start_time'],
                    end_time = request.POST['end_time'],
                )
                project.save()
                save_uploaded(request, composition)
            return HttpResponse('add successfully')
        else:
            form = ProjectForm()
            return render(request, 'account/add_project.html', {'form':form, 'invalid':True})


@login_required()
#@permission_required('account.verified_expert_permission', raise_exception=True)
def add_paper(request):
    if request.method == 'GET':
        form = PaperForm()
        return render(request, 'account/add_paper.html', {'form':form, 'invalid':False})
    else:
        form = PaperForm(request.POST, request.FILES)
        if form.is_valid():
            with database_transaction.atomic():
                composition = create_composition(request)                
                paper = Paper.objects.create(
                    composition = composition,
                    abstract = request.POST['abstract'],
                    keywords = request.POST['keywords'],
                )
                paper.save()
                save_uploaded(request, composition)                
            return HttpResponse('add successfully')
        else:
            form = PaperForm()
            return render(request, 'account/add_paper.html', {'form':form, 'invalid':True})

@login_required()
#@permission_required('account.verified_expert_permission', raise_exception=True)
def add_patent(request):
    if request.method == 'GET':
        form = PatentForm()
        return render(request, 'account/add_patent.html', {'form':form, 'invalid':False})
    else:
        form = PatentForm(request.POST, request.FILES)
        if form.is_valid():
            with database_transaction.atomic():
                composition = create_composition(request)
                patent = Patent.objects.create(
                    composition = composition,
                    patent_no = request.POST['patent_no'],
                    apply_time = request.POST['apply_time'],
                    auth_time = request.POST['auth_time'],
                )
                patent.save()
                save_uploaded(request, composition)
                
            return HttpResponse('add successfully')
        else:
            form = PatentForm()
            return render(request, 'account/add_patent.html', {'form':form, 'invalid':True})

@login_required()
#@permission_required('account.verified_expert_permission', raise_exception=True)
def show_composition_list(request):
    expert = request.user.expertuser_relation
    composition_list = Composition.objects.filter(expert = expert)

    return render(request, 'account/show_composition_list.html', {'composition_list' : composition_list})

# returns a (type, relevant_entity) pair
def get_composition_type(composition):
    try:
        project = composition.project
        return ('project', project)
    except Project.DoesNotExist:
        try:
            patent = composition.patent
            return ('patent', patent)
        except Patent.DoesNotExist:
            try:
                paper = composition.paper
                return ('paper', paper)
            except:
                assert False

@login_required()
#@permission_required('account.verified_expert_permission', raise_exception=True)
def composition_detail(request, pk):
    expert = request.user.expertuser_relation
    exist = True
    try:
        comp = Composition.objects.filter(expert=expert).get(pk=pk)
    except Composition.DoesNotExist:
        return render(request, 'account/composition_detail.html', {'exist': False})
    
    #appendixes = comp.appendix.objects.all()
    appendixes = Appendix.objects.filter(composition_id=comp.pk)
    #for_display = comp.displaymaterial.objects.all()
    for_display = DisplayMaterial.objects.filter(composition_id=comp.pk)

    pair = get_composition_type(comp)

    return render(request, 'account/composition_detail.html', 
                    {'exist': True, 'appendixes': appendixes, 'for_display': for_display,
                     'comp': comp, 'ty': pair[0], 'body': pair[1]})


@login_required()
#@permission_required('account.verified_expert_permission', raise_exception=True)
def delete_composition(request, pk):
    if request.method == 'GET':
        composition = Composition.objects.filter(pk = pk)
        if composition.count() == 0:
            return HttpResponse('成果8存在')
        return render(request, 'account/delete_composition.html', {'composition':composition[0]})
    elif request.method == 'POST':
        Composition.objects.filter(pk = pk).delete()
        return HttpResponse('delete success')
'''
