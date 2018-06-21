from django.http import HttpResponse
from django.db.models import Sum
from display.models import *
import json


def expert_detail(request):
    expert_account=request.user.expertuser_relation
    expert=ExpertDetail.objects.get(account=expert_account)
    name=expert.name
    institute=expert.institute.inst_name
    paper_list = expert.papers.all()
    count_journal=paper_list.filter(doc_type='Journal').count()
    count_conference=paper_list.filter(doc_type='Conference').count()
    count_book=paper_list.filter(doc_type='Book').count()
    count_other=paper_list.exclude(doc_type__in=['Journal', 'Conference', 'Book']).count()
    count_paper=paper_list.all().count()
    count_citation=paper_list.all().aggregate(count_citation=Sum('n_citation')).get('count_citation')
    cooperation = []
    for paper in paper_list:
        authors = paper.authors.all().exclude(name=name)
        for author in authors:
            if author not in cooperation:
                cooperation.append(author.name)

    j_str={'expert_name':name,'expert_institute':institute,'count_journal':count_journal,
           'count_conference':count_conference,'count_book':count_book,'count_other':count_other,
           'count_paper':count_paper,'count_citation':count_citation,'cooperation':cooperation}

    return HttpResponse(json.dumps(j_str), content_type="application/json")

def paper_detail(request,id):
    expert_account = request.user.expertuser_relation
    expert=ExpertDetail.objects.get(account=expert_account)
    paper_list = expert.papers.all()

    try:
        paper=paper_list.get(id=id)
    except Paper.DoesNotExist:
        return HttpResponse('Paper does not exist!')

    authors=paper.authors.all()
    author_name = []
    for author in authors:
        if author not in author_name:
            author_name.append(author.name)

    keywords=paper.keywords.all()
    keywords_name = []
    for keyword in keywords:
        if keyword not in keywords_name:
            keywords_name.append(keyword.word)

    studyareas=paper.fos.all()
    studyarea_name = []
    for studyarea in studyareas:
        if studyarea not in studyarea_name:
            studyarea_name.append(studyarea.Area_name)

    abstract=paper.abstract
    count_citation=paper.n_citation
    references=(paper.references)

    j_str={'authors':author_name,'abstract':abstract,'keywords':keywords_name,
           'study_area':studyarea_name,'count_citation':count_citation,'references':references}

    return HttpResponse(json.dumps(j_str), content_type="application/json")
