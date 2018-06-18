from django.shortcuts import render
from .models import Transaction
from display.models import Paper
from django.http.response import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction as database_transaction

'''
@login_required(login_url = '/account/login/')
@permission_required('account.verified_commuser_permission', login_url = '/account/login/', raise_exception=True)
def trans_info (request, pk):
    try:
        require_composition = Composition.objects.get(pk = pk)
    except Composition.DoesNotExist:
        return HttpResponse("the composition you require is not exist")
    
    return render(request, 'buy/trans_info.html', {'composition' : require_composition})

@login_required(login_url = '/account/login/')
@permission_required('account.verified_commuser_permission', login_url = '/account/login/', raise_exception=True)
def applicate_transact(request, pk):
    if request.method == 'POST':
        try:
            require_composition = Composition.objects.get(pk = pk)
        except Composition.DoesNotExist:
            return HttpResponse("the composition you require is not exist")
        
        check_transaction = Transaction.objects.filter(trans_composition = require_composition, trans_user = request.user.commuser_relation)
        if check_transaction is not None:
            return HttpResponse("there is alread a same transaction in your account!")
        
        new_transaction = Transaction()
        new_transaction.app_date = timezone.now()
        new_transaction.trans_user = request.user.commuser_relation
        new_transaction.trans_composition = require_composition
        new_transaction.trans_price = require_composition.price
        new_transaction.save()
        return redirect('/buy/translist')
    else:
        return HttpResponse("what are you fucking doing!")

@login_required(login_url = '/account/login/')
@permission_required('account.verified_commuser_permission', login_url = '/account/login/', raise_exception=True)
def trans_list(request):
    user = request.user.commuser_relation
    transaction_list = Transaction.objects.filter(trans_user = user)
    #need an order by

    return render(request, 'buy/trans_list.html', {'transaction_list': transaction_list})

@login_required(login_url = '/account/login/')
@permission_required('account.verified_commuser_permission  ', login_url = '/account/login/', raise_exception=True)
def bought_item(request, pk):
    user = request.user.commuser_relation
    try:
        trans = Transaction.objects.get(pk = pk)
    except Transaction.DoesNotExist:
        return HttpResponse("The transaction doesn't exist")
    if trans.trans_user != user:
        return HttpResponse("The transaction doesn't belong to you")
    if request.method == 'POST':
        commuser = request.user.commuser_relation
        if commuser.credit >= trans.trans_price: 
            with database_transaction.atomic():
                commuser.credit = commuser.credit - trans.trans_price
                commuser.save()
                trans.is_paid = True
                trans.save()
        else:
            return HttpResponse("you are poor!")
    return render(request, 'buy/bought_item.html', {'transaction' : trans})


#expert module next:

@login_required(login_url = '/account/login/')
@permission_required('account.verified_expert_permission', login_url = '/account/login/', raise_exception=True)
def expert_trans_list(request):
    user = request.user.expertuser_relation
    transaction_list = Transaction.objects.filter(trans_composition__expert = user)

    return render(request, 'buy/expert_trans_list.html', {'transaction_list' : transaction_list})

@login_required(login_url = '/account/login/')
@permission_required('account.verified_expert_permission', login_url = '/account/login/', raise_exception=True)
def accept_trans(request, pk):
    try:
        trans = Transaction.objects.get(pk = pk)
    except Transaction.DoesNotExist:
        return HttpResponse("The transaction does't exist")
    if trans.trans_composition.expert != request.user.expertuser_relation:
        return HttpResponse("THe transaction doesn't belong to you")
    
    if request.method == 'POST':
        trans.is_accept = True
        trans.save()
    return render(request, "buy/accept_trans.html", {'transaction' : trans})
'''