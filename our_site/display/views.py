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
from display.models import *
from account.models import *

'''
def display_index(request,epk):
    latest_composition_list = Composition.objects.filter(expert=epk).order_by('-upload_time')[:3]
    return render(request, 'display/index.html',{'latest_composition_list':latest_composition_list})

def show_composition_list(request):
    expert = request.user.expertuser_relation
    composition_list = Composition.objects.filter(expert = expert)

    return render(request, 'display/show_composition_list.html', {'composition_list' : composition_list})

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


def composition_detail(request, pk):
    expert = request.user.expertuser_relation
    exist = True
    try:
        comp = Composition.objects.filter(expert=expert).get(pk=pk)
    except Composition.DoesNotExist:
        return render(request, 'display/composition_detail.html', {'exist': False})

    # appendixes = comp.appendix.objects.all()
    appendixes = Appendix.objects.filter(composition_id=comp.pk)
    # for_display = comp.displaymaterial.objects.all()
    for_display = DisplayMaterial.objects.filter(composition_id=comp.pk)

    pair = get_composition_type(comp)

    return render(request, 'display/composition_detail.html',
                  {'exist': True, 'appendixes': appendixes, 'for_display': for_display,
                   'comp': comp, 'ty': pair[0], 'body': pair[1]})
'''