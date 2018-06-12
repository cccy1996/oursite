from django.shortcuts import render
from .models import Question
from display.models import Composition
from django.http.response import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction as database_transaction
from account.models import Commuser_relation
from django.contrib.auth.models import User


def question_index(request):
    return render(request, 'question/index.html')


@login_required(login_url='/account/login/')
def consumer_ask_question(request):
    if request.method == 'GET':
        return render(request, 'question/ask_question.html', {'username': request.user.username})
    elif request.method == 'POST':
        question_title = request.POST['question_title']
        question_content = request.POST['question_content']

        if question_title != '':
            question = Question()
            question.que_title = question_title
            question.que_content = question_content
            question.que_user = Commuser_relation.objects.get(pk=request.user.id)
            question.save()
            return redirect('/question')
        else:
            return HttpResponse("title cannot be null")
    else:
        return HttpResponse("what are you fucking doing!")


@login_required(login_url='/account/login/')
def consumer_question_detail(request, queid):
    try:
        question = Question.objects.get(pk=queid)
        result = {'question': question.que_info(),
                  'query_error': False}
    except Question.DoesNotExist:
        result = {'query_error': True}
    return render(request, 'question/question_detail.html', result)


@login_required(login_url='/account/login/')
def expert_answer_question(request, pk):
    return 1


@login_required(login_url='/account/login/')
def consumer_question_list(request, quetype): #待回答/已回答
    if quetype not in [0, 1]:
        return HttpResponse("quetype must be 0 or 1")
    questions = Question.objects.filter(que_user__user=request.user, ans_status=quetype)
    results = []
    for que in questions:
        results.append(que.que_info())
    return render(request, 'question/consumer_question_list.html', {'que_list': results})


@login_required(login_url='/account/login/')
def expert_question_list(request, eid, quetype): #待回答/已回答
    #username = request.user.commuser_ralation.username
    questions = Question.objects.filter(ans_expert__id=eid)
    results = []
    for que in questions:
        results.append(que.que_info())
        print(que.que_info())
    print(results)
    return HttpResponse(results)


def view_free_question_list(): #查看免费问答
    return 1


def view_question_list():
    return 1
