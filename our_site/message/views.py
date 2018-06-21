from django.shortcuts import render
# Create your views here.
from .models import Inbox, User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import redirect
from django.template import loader
import json
from django.core import serializers


def message_index(request):
    return render(request, 'message/index.html')


@login_required(login_url='/account/login/')
def send_message(request):
    if request.method == 'GET':
        msg1 = {'username': request.user.username}
        return HttpResponse(json.dumps(msg1), content_type="application/json")
        # return render(request, 'message/send_message.html', {'username': request.user.username})
    elif request.method == 'POST':
        message_to = request.POST['to_whom']
        message_content = request.POST['message_content']
        if message_to == '':
            msg2 = {'msg': "whom do you want to send message to?"}
            return HttpResponse(json.dumps(msg2), content_type="application/json")
            # return HttpResponse("whom do you want to send message to?")

        else:
            try:
                User.objects.get(username=message_to)
                inbox = Inbox()
                inbox.inbox_content = message_content
                inbox.inbox_sender = request.user
                inbox.inbox_receiver = User.objects.get(username=message_to)
                inbox.inbox_date = timezone.now()
                inbox.save()
                return redirect('/message')
            except Exception:
                msg3 = {'msg':"there is no people named %s" % message_to}
                return HttpResponse(json.dumps(msg3), content_type="application/json")
                # return HttpResponse("there is no people named %s" % message_to)


@login_required(login_url='/account/login/')
def read_message(request):
    # message_list = Inbox.objects.filter(inbox_receiver=request.user)
    '''
    template = loader.get_template('message/read_message.html')
    context = {
        'message_list':
    }
    '''
    messages = Inbox.objects.filter(inbox_receiver=request.user)
    li = []
    for m in messages:
        obj = {
            'inbox_id' : m.inbox_id,
            'inbox_date' : m.inbox_date,
            'inbox_sender' : m.inbox_sender,
            'inbox_receiver' : m.inbox_receiver,
            'inbox_content' : m.inbox_content,
        }
        li.append(obj)

    # json_data = serializers.serialize("json", Inbox.objects.filter(inbox_receiver=request.user))
    #return HttpResponse(json_data, content_type="application/json")
    # return HttpResponse(template.render(context, request))
    return HttpResponse(json.dumps(li), content_type="application/json")
