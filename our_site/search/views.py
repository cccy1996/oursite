from django.shortcuts import render, redirect
from django.http import HttpResponse
import nltk
from display.models import Paper
from django.db.models import Q, F
from django.core import serializers
import json

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
    page = int(request.GET['page'])
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
        json_data = json.dumps(data)
        '''
        with open('/home/elin/file.json', 'w') as out:
            out.write(json_data)
        '''

        return HttpResponse(json_data, content_type="application/json")
        #return render(request, 'search/search_list.html', {'paper_list' : related_paper})
    else:
        all_empty = True
        order = request.GET['order']
        author = request.GET['author']
        doc_type = request.GET['type']
        publisher = request.GET['publisher']
        start_year = request.GET['start_year']
        end_year = request.GET['end_year']
        keywords = request.GET['keyword'].strip(' ').split(',')
        keywords = list(set(keywords)) # unique
        # print(keywords)

        hit_times = dict()
        paper_list = Paper.objects.none()
        for kwd in keywords:
            papers = Paper.objects.filter(Q(keywords__word__icontains = kwd) 
                        | Q(chunkfromtitle__chunk__icontains = kwd)).distinct()
            for p in papers:
                if p in hit_times:
                    hit_times[p.pk] += 1
                else:
                    hit_times[p.pk] = 1
            paper_list = paper_list.union(papers)

        if request.GET['keyword'] != '':
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
        paper_list = sorted(paper_list, key=lambda x: hit_times[x.pk], reverse=True)
        if order == 'citation':
            paper_list.sort(key = lambda x : x.n_citation if x.n_citation is not None else 0, reverse = True)
        elif order == 'year':
            paper_list.sort(key = lambda x : x.year, reverse = True)
            
        paper_list = paper_list[20*page:20*(1+page)]
    
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
        json_data = json.dumps(data)
        
        return HttpResponse(json_data, content_type="application/json")
        # return render(request, 'search/search_list.html', {'paper_list' : paper_list})
