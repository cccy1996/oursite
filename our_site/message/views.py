from django.shortcuts import render
# Create your views here.
from .models import Inbox, User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import redirect
from django.template import loader


def message_index(request):
    return render(request, 'message/index.html')


@login_required(login_url='/account/login/')
def send_message(request):
    if request.method == 'GET':
        return render(request, 'message/send_message.html', {'username': request.user.username})
    elif request.method == 'POST':
        message_to = request.POST['to_whom']
        message_content = request.POST['message_content']
        if message_to == '':
            return HttpResponse("whom do you want to send message to?")

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
                return HttpResponse("there is no people named %s" % message_to)


@login_required(login_url='/account/login/')
def read_message(request):
    message_list = Inbox.objects.all()
    template = loader.get_template('message/read_message.html')
    context = {
        'message_list': message_list
    }
    return HttpResponse(template.render(context, request))
