from django.shortcuts import render, redirect
from django.http import HttpResponse
import nltk
from display.models import *
from django.db.models import Q, F
from django.core import serializers
import json
from django.db.models import Count
import math

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


def search_list(request):
    choice = request.GET['search_type']
    try:
        page = int(request.GET['page'])
    except KeyError:
        page = 0

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
        npages = len(related_paper) // 20 + 1
        related_paper = related_paper[20*page:20*(1+page)]
        
        
        data = []
        for paper in related_paper:
            js = {
                'title' : paper.title, 'paper_id' : paper.id, 'year': paper.year,
                'doc_type' : paper.doc_type, 'n_citation' : paper.n_citation, 
                'publisher' : paper.publisher, 'authors' : list(),
            }
            for author in paper.authors.all():
                js['authors'].append({
                    'name' : author.name, 'id': author.custompk,
            })
            data.append(js)
        pageddata = {'data': data, 'pages': npages,}
        json_data = json.dumps(pageddata)
        '''
        with open('/home/elin/file.json', 'w') as out:
            out.write(json_data)
        '''

        return HttpResponse(json_data, content_type="application/json")
        #return render(request, 'search/search_list.html', {'paper_list' : related_paper})
    else:
        all_empty = True
        order = request.GET['order'].strip(' ')
        author = request.GET['author'].strip(' ')
        doc_type = request.GET['type'].strip(' ')
        publisher = request.GET['publisher'].strip(' ')
        try:
            start_year = int(request.GET['start_year'])
        except ValueError:
            start_year = 0
        try:
            end_year = int(request.GET['end_year'])
        except ValueError:
            end_year = 2100
        keywordstr = request.GET['keyword'].strip(' ')
        if len(keywordstr) > 0:
            keywords = keywordstr.split(',')
            keywords = list(set(keywords)) # unique
            hit_times = dict()
            paper_list = Paper.objects.none()
            for kwd in keywords:
                papers = Paper.objects.filter(Q(keywords__word__icontains = kwd) 
                        | Q(chunkfromtitle__chunk__icontains = kwd)).distinct()
                for p in papers:
                    if p.pk in hit_times:
                        hit_times[p.pk] += 1
                    else:
                        hit_times[p.pk] = 1
                paper_list = paper_list.union(papers)
        else:
            keywords = []
            paper_list = Paper.objects.all()
        # print(keywords)

        if len(keywordstr) > 0:
            all_empty = False

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
        
        # it's not a queryset anymore
        if len(keywordstr) > 0:
            paper_list = sorted(paper_list, key=lambda x: hit_times[x.pk], reverse=True)
            if order == 'citation':
                paper_list.sort(key = lambda x : x.n_citation if x.n_citation is not None else 0, reverse = True)
            elif order == 'year':
                paper_list.sort(key = lambda x : x.year, reverse = True)
        else:
            if order == 'citation':
                paper_list = paper_list.order_by('-n_citation')
            elif order == 'year':
                paper_list = paper_list.order_by('-year')
        
        npages = len(paper_list)//20 + 1
        related_paper = paper_list[20*page:20*(1+page)]
    
        if all_empty == True:
            return redirect('/search/')
        
        data = []
        for paper in related_paper:
            js = {
                'title' : paper.title, 'paper_id' : paper.id, 'year': paper.year,
                'doc_type' : paper.doc_type, 'n_citation' : paper.n_citation, 
                'publisher' : paper.publisher, 'authors' : list(),
            }
            for author in paper.authors.all():
                js['authors'].append({
                    'name' : author.name, 'id': author.custompk,
            })
            data.append(js)
        pageddata = {'data': data, 'pages': npages,}
        json_data = json.dumps(pageddata)
        
        return HttpResponse(json_data, content_type="application/json")
        # return render(request, 'search/search_list.html', {'paper_list' : paper_list})

def heat_analysis(request):
    #在这里需要返回 最火的filed 和 最火的paper
    area_list = StudyArea.objects.annotate(num_paper = Count('related_paper')).order_by('-num_paper')[:5]
    paper_list = Paper.objects.all().order_by('-n_citation')[:5]
    data = {
        'area_list' : list(),
        'paper_list' : list(),
    }
    for area in area_list:
        data['area_list'].append(
            {'area_name' : area.Area_name}
        )
    
    for paper in paper_list:
        data['paper_list'].append(
            {'title': paper.title, 'paper_id' : paper.id, 'n_citation': paper.n_citation}
        )
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")