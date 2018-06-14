from django.shortcuts import render
from .models import Question
from display.models import Composition
from django.http.response import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction as database_transaction
from account.models import Commuser_relation, Expertuser_relation
from django.contrib.auth.models import User


def question_index(request):
    return render(request, 'question/index.html')


@login_required(login_url='/account/login/')
@permission_required('account.commuser_permission')
def consumer_ask_question(request):
    if request.method == 'GET':
        return render(request, 'question/ask_question.html', {'username': request.user.username})
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
            return HttpResponse("title and expertID cannot be null")
    else:
        return HttpResponse("what are you fucking doing!")


@login_required(login_url='/account/login/')
def question_list(request, quetype):
    if quetype not in [0, 1]:
        return HttpResponse("quetype must be 0 or 1")
    if request.user.has_perm('account.commuser_permission'):
        questions = Question.objects.filter(que_user__user=request.user, ans_status=quetype)
    elif request.user.has_perm('account.expert_permission'):
        questions = Question.objects.filter(ans_expert__user=request.user, ans_status=quetype)
    else:
        return HttpResponse("you don't have permission")
    results = []
    for que in questions:
        results.append(que.que_info())
    return render(request, 'question/question_list.html', {'que_list': results})


@login_required(login_url='/account/login/')
def question_detail(request, queid):
    try:
        question = Question.objects.get(pk=queid)
        result = {'question': question.que_info(),
                  'query_error': False}
    except Question.DoesNotExist:
        result = {'query_error': True}
        return render(request, 'question/question_detail.html', result)

    if request.user.has_perm('account.expert_permission') and question.ans_status == 0:
        return render(request, 'question/answer_question.html', result)
    else:
        return render(request, 'question/question_detail.html', result)


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
            return HttpResponse("问题不存在？？？")
    else:
        return HttpResponse("答案不能为空")