from django.shortcuts import render, redirect
from django.http import HttpResponse
import nltk
from display.models import Paper

def search(request):
    return render(request, 'search/search.html')


def search_list(request):
    choice = request.GET['search_type']
    if choice == 'simple':
        text_list = nltk.word_tokenize(request.GET['simple_search'])
        paper_list = Paper.objects.all()

        #这里应该被改写成主题搜索
        for text in text_list:
            paper_list = paper_list.filter(keywords__word = text)
        paper_list = paper_list.order_by('-n_citation')
        
        return render(request, 'search/search_list.html', {'paper_list' : paper_list})
    else:
        all_empty = True
        paper_list = Paper.objects.all()
        text_list = nltk.word_tokenize(request.GET['keyword'])
        author = request.GET['author']
        doc_type = request.GET['type']
        publisher = request.GET['publisher']
        start_year = request.GET['start_year']
        end_year = request.GET['end_year']

        if request.GET['keyword'] != '':
            all_empty = False

        for text in text_list:
            paper_list = paper_list.filter(keywords__word = text)

        if author != '':
            all_empty = False
            paper_list = paper_list.filter(authors__name = author)

        if doc_type != 'null':
            paper_list = paper_list.filter(doc_type = doc_type)

        if publisher != '':
            all_empty = False
            paper_list = paper_list.filter(publisher = publisher)
            
        if start_year != '' and end_year != '':
            all_empty = False
            paper_list = paper_list.filter(year__gte = start_year, year__lte = end_year)
        

        paper_list = paper_list.order_by('-n_citation')
        if all_empty == True:
            return redirect('/search/')
        return render(request, 'search/search_list.html', {'paper_list' : paper_list})
