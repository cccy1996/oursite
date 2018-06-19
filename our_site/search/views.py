from django.shortcuts import render, redirect
from django.http import HttpResponse
import nltk
from display.models import Paper
from django.db.models import Q, F

def relation_add(relations, paper):
    if paper.pk in relations:
        relations[paper.pk] += 1
    else:
        relations[paper.pk] = 1

def process_relation(relations, percent):
    #max_relativity = max(relations, key=relations.get)
    max_relativity = 0
    for r in relations:
        if max_relativity < relations[r]:
            max_relativity = relations[r]
    for r in list(relations):
        if relations[r] < max_relativity * percent:
            relations.pop(r)

def get_list(relations):
    sorted_relations = sorted(relations, key = lambda x : relations[x], reverse = True)
    related_paper = list()
    for r in sorted_relations:
        related_paper.append(Paper.objects.get(pk = r))
    return related_paper


def search(request):
    return render(request, 'search/search.html')


def search_list(request, page = 0):
    choice = request.GET['search_type']
    if choice == 'simple':
        text_list = nltk.word_tokenize(request.GET['simple_search'])
        order = request.GET['order']
        
        paper_list = Paper.objects.all()
        relations = dict()

        for text in text_list:
            relation_list = paper_list.filter(title__icontains = text)
            for paper in relation_list:
                relation_add(relations, paper)
        process_relation(relations, 0.3)
        related_paper = get_list(relations)

        if order == 'citation':
            related_paper.sort(key = lambda x : x.n_citation if x.n_citation is not None else 0, reverse = True)
        elif order == 'year':
            related_paper.sort(key = lambda x : x.year, reverse = True)
        else:
            pass
        related_paper = related_paper[20*page:20*(1+page)]
        
        return render(request, 'search/search_list.html', {'paper_list' : related_paper})
    else:
        all_empty = True
        paper_list = Paper.objects.all()
        text_list = nltk.word_tokenize(request.GET['keyword'])
        order = request.GET['order']
        author = request.GET['author']
        doc_type = request.GET['type']
        publisher = request.GET['publisher']
        start_year = request.GET['start_year']
        end_year = request.GET['end_year']

        if request.GET['keyword'] != '':
            all_empty = False

        for text in text_list:
            paper_list = paper_list.filter(Q(keywords__word__icontains = text) | Q(chunkfromtitle__chunk__icontains = text)).distinct()

        if author != '':
            all_empty = False
            paper_list = paper_list.filter(authors__name__icontains = author)

        if doc_type != 'null':
            paper_list = paper_list.filter(doc_type = doc_type)

        if publisher != '':
            all_empty = False
            paper_list = paper_list.filter(publisher__icontains = publisher)
            
        if start_year != '' and end_year != '':
            all_empty = False
            paper_list = paper_list.filter(year__gte = start_year, year__lte = end_year).distinct()
        elif start_year == '' and end_year != '':
            all_empty = False
            paper_list = paper_list.filter(year__lte = end_year)
        elif start_year != '' and end_year == '':
            all_empty = False
            paper_list = paper_list.filter(year__gte = start_year)
        
        
        
        if order == 'citation':
            paper_list = paper_list.order_by('-n_citation')
        elif order == 'year':
            paper_list = paper_list.order_by('-year')
        else:
            pass
            #这里需要做一个相关度排序
        paper_list = paper_list[20*page:20*(1+page)]
    
        if all_empty == True:
            return redirect('/search/')
        return render(request, 'search/search_list.html', {'paper_list' : paper_list})
