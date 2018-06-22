from django.http import HttpResponse
from django.db.models import Sum
from display.models import *
import json


def expert_detail(request,id):
    #expert_account=request.user.expertuser_relation
    expert=ExpertDetail.objects.get(custompk=id)
    name=expert.name
    institute=expert.institute.inst_name
    paper_list = expert.papers.all()
    count_journal=paper_list.filter(doc_type='Journal').count()
    count_conference=paper_list.filter(doc_type='Conference').count()
    count_book=paper_list.filter(doc_type='Book').count()
    count_other=paper_list.exclude(doc_type__in=['Journal', 'Conference', 'Book']).count()
    count_paper=paper_list.all().count()
    count_citation=paper_list.all().aggregate(count_citation=Sum('n_citation')).get('count_citation')
    cooperation_id = []
    for paper in paper_list:
        authors = paper.authors.all().exclude(name=name)
        for author in authors:
            if author not in cooperation_id:
                cooperation_id.append(author.custompk)

    cooperation_name = []
    for paper in paper_list:
        authors = paper.authors.all().exclude(name=name)
        for author in authors:
            if author not in cooperation_name:
                cooperation_name.append(author.name)

    paper_id_list=[]
    paper_title_list=[]
    for paper in paper_list:
        paper_id_list.append(paper.id)
        paper_title_list.append(paper.title)

    studyarea_name = []
    for paper in paper_list:
        studyareas=paper.fos.all()
        for studyarea in studyareas:
            if studyarea not in studyarea_name:
                studyarea_name.append(studyarea.Area_name)

    j_str={'expert_name':name,'expert_institute':institute,'count_journal':count_journal,
           'count_conference':count_conference,'count_book':count_book,'count_other':count_other,
           'count_paper':count_paper,'count_citation':count_citation,'cooperation_id':cooperation_id,
           'cooperation_name':cooperation_name,'paper_id_list':paper_id_list,'paper_title_list':paper_title_list,'studyarea_name':studyarea_name}

    return HttpResponse(json.dumps(j_str), content_type="application/json")

def paper_detail(request,id):
    #expert_account = request.user.expertuser_relation
    #expert=ExpertDetail.objects.get(custompk=expert_account)
    paper_list = Paper.objects.all()
    try:
        paper=Paper.objects.get(pk=id)
    except Paper.DoesNotExist:
        return HttpResponse('Paper does not exist!')

    authors=paper.authors.all()
    author_name = []
    for author in authors:
        author_name.append(author.name)

    author_id = []
    for author in authors:
        author_id.append(author.custompk)

    keywords=paper.keywords.all()
    keywords_name = []
    for keyword in keywords:
        keywords_name.append(keyword.word)

    studyareas=paper.fos.all()
    studyarea_name = []
    for studyarea in studyareas:
        studyarea_name.append(studyarea.Area_name)

    abstract=paper.abstract
    if paper.n_citation is not None:
        count_citation = paper.n_citation
    else:
        count_citation = 0
    references=(paper.references)
    paper_title=paper.title
    j_str={'paper_title':paper_title,'author_id':author_id,'author_name':author_name,'abstract':abstract,'keywords':keywords_name,
           'study_area':studyarea_name,'count_citation':count_citation,'references':references}

    return HttpResponse(json.dumps(j_str), content_type="application/json")
