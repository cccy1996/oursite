from django.shortcuts import render
from .models import Question
from django.http.response import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction as database_transaction
from account.models import Commuser_relation, Expertuser_relation
from django.contrib.auth.models import User
import json

def question_index(request):
    return render(request, 'question/index.html')


@login_required(login_url='/account/login/')
@permission_required('account.commuser_permission')
def consumer_ask_question(request):
    if request.method == 'GET':
        msg1 = {'username': request.user.username}
        return HttpResponse(json.dumps(msg1), content_type="application/json")
        # return render(request, 'question/ask_question.html', {'username': request.user.username})
    elif request.method == 'POST':
        question_title = request.POST['question_title']
        question_content = request.POST['question_content']
        expert_id = request.POST['expert_id']

        if question_title != '' and expert_id != '':
            question = Question()
            with database_transaction.atomic():
                question.que_title = question_title
                question.que_content = question_content
                question.que_user = Commuser_relation.objects.get(pk=request.user.id)
                question.ans_expert = Expertuser_relation.objects.get(pk=int(expert_id))
                question.save()
            return redirect('/question')
        else:
            msg2 = {'msg': "title and expertID cannot be null"}
            return HttpResponse(json.dumps(msg2), content_type="application/json")
            # return HttpResponse("title and expertID cannot be null")
    else:
        msg3 = {'msg': "what are you fucking doing!"}
        return HttpResponse(json.dumps(msg3), content_type="application/json")
        # return HttpResponse("what are you fucking doing!")


@login_required(login_url='/account/login/')
def question_list(request, quetype):
    if quetype not in [0, 1]:
        msg4 = {'msg': "quetype must be 0 or 1"}
        return HttpResponse(json.dumps(msg4), content_type="application/json")
        # return HttpResponse("quetype must be 0 or 1")
    if request.user.has_perm('account.commuser_permission'):
        questions = Question.objects.filter(que_user__user=request.user, ans_status=quetype)
    elif request.user.has_perm('account.expert_permission'):
        questions = Question.objects.filter(ans_expert__user=request.user, ans_status=quetype)
    else:
        msg5 = {'msg':"you don't have permission"}
        return HttpResponse(json.dumps(msg5), content_type="application/json")
        # return HttpResponse("you don't have permission")
    results = []
    for que in questions:
        results.append(que.que_info())
    msg6 = {'que_list': results}
    return HttpResponse(json.dumps(msg6), content_type="application/json")
    # return render(request, 'question/question_list.html', {'que_list': results})


@login_required(login_url='/account/login/')
def question_detail(request, queid):
    try:
        question = Question.objects.get(pk=queid)
        msg7 = {'question': question.que_info(),
                  'query_error': False}
    except Question.DoesNotExist:
        # result = {'query_error': True}
        msg7 = {'query_error': True}
        return HttpResponse(json.dumps(msg7), content_type="application/json")
        # return render(request, 'question/question_detail.html', result)

    if request.user.has_perm('account.expert_permission') and question.ans_status == 0:
        return HttpResponse(json.dumps(msg7), content_type="application/json")
        # return render(request, 'question/answer_question.html', result)
    else:
        return HttpResponse(json.dumps(msg7), content_type="application/json")
        # return render(request, 'question/question_detail.html', result)


@login_required(login_url='/account/login/')
def expert_answer_question(request, queid):
    answer_content = request.POST['answer_content']

    if answer_content != '':
        try:
            question = Question.objects.get(pk=queid)
            with database_transaction.atomic():
                question.ans_content = answer_content
                question.ans_status = 1
                question.save()
            return redirect('/question')
        except Question.DoesNotExist:
            msg8 = {'msg': "问题不存在？？？"}
            return HttpResponse(json.dumps(msg8), content_type="application/json")
            # return HttpResponse("问题不存在？？？")
    else:
        msg9 = {'msg': "答案不能为空"}
        return HttpResponse(json.dumps(msg9), content_type="application/json")
        # return HttpResponse("答案不能为空")