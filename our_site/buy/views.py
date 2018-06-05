from django.shortcuts import render
from .models import Transaction
from display.models import Composition
from django.http.response import HttpResponse
from django.utils import timezone

def transact(request, pk):
    pass
    '''
    try:
        require_composition = Composition.objects.get(pk = pk)
    except Exception:
        return HttpResponse("the composition you require is not exist")
    
    new_transaction = Transaction(app_date = timezone.now())
    new_transaction.trans_user = request.user.commuser_relation
    new_transaction.trans_composition = require_composition
    new_transaction.trans_price = require_composition.price
    new_transaction.save()
    return render(request, 'buy/transact.html', {'new_transaction' : new_transaction})
    '''