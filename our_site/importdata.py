import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "our_site.settings") 
import django
django.setup()

from display.models import *
from django.db import transaction
import json

def add_authors(paper, data):
    for author in data['authors']:
        if 'org' in author:
            s_institute = Institute.objects.filter(inst_name = author['org'])
            
            if len(s_institute) == 1:
                try:
                    s_author = ExpertDetail.objects.get(name = author['name'], institute = s_institute[0])
                    paper.authors.add(s_author)
                except Exception:
                    expert = ExpertDetail(name = author['name'], institute = s_institute[0])
                    expert.save()
                    paper.authors.add(expert)
            else:
                n_institute = Institute(inst_name = author['org'])
                n_institute.save()
                expert = ExpertDetail(name = author['name'], institute = n_institute)
                expert.save()
                paper.authors.add(expert)
        else:
            empty_institute = Institute.objects.get(inst_name = 'for empty')
            s_author = ExpertDetail.objects.filter(name = author['name'], institute = empty_institute)
            if len(s_author) == 1:
                    paper.authors.add(s_author[0])
            else:
                expert = ExpertDetail(name = author['name'], institute = empty_institute)
                expert.save()
                paper.authors.add(expert)
def add_keywords(paper, data):
    if 'keywords' not in data:
        return
    for keyword in data['keywords']:
        s_keyword = Keyword.objects.filter(word = keyword)
        if len(s_keyword) == 1:
            paper.keywords.add(s_keyword[0])
        else:
            n_keyword = Keyword(word = keyword)
            n_keyword.save()
            paper.keywords.add(n_keyword)
def add_fos(paper, data):
    if 'fos' not in data:
        return
    for field in data['fos']:
        s_studyarea = StudyArea.objects.filter(Area_name = field)
        if len(s_studyarea) == 1:
            paper.fos.add(s_studyarea[0])
        else:
            n_studyarea = StudyArea(Area_name = field)
            n_studyarea.save()
            paper.fos.add(n_studyarea)
def add_venue(paper, data):
    if 'venue' not in data:
        return
    paper.venue = data['venue']
def add_n_citation(paper, data):
    if 'n_citation' not in data:
        return
    paper.n_citation = data['n_citation']
def add_references(paper, data):
    if 'references' not in data:
        return
    paper.references = data['references']
def add_page_start(paper, data):
    if 'page_start' not in data:
        return
    paper.page_start = int(data['page_start'])
def add_page_end(paper, data):
    if 'page_end' not in data:
        return
    paper.page_end = int(data['page_end'])
def add_doc_type(paper, data):
    if 'doc_type' not in data:
        return
    paper.doc_type = data['doc_type']
def add_lang(paper, data):
    if 'lang' not in data:
        return
    paper.lang = data['lang']
def add_publisher(paper, data):
    if 'publisher' not in data:
        return
    paper.publisher = data['publisher']
def add_issn(paper, data):
    if 'issn' not in data:
        return
    paper.issn = data['issn']
def add_isbn(paper, data):
    if 'isbn' not in data:
        return
    paper.isbn = data['isbn']
def add_doi(paper, data):
    if 'doi' not in data:
        return
    paper.doi = data['doi']
def add_pdf(paper, data):
    if 'pdf' not in data:
        return
    paper.pdf = data['pdf']
def add_url(paper, data):
    if 'url' not in data:
        return
    paper.url = data['url']
def add_abstract(paper, data):
    if 'abstract' not in data:
        return
    paper.abstract = data['abstract']


def main(data_path, lines):
    json_file = open(data_path, 'r', 1)
    for i in range(lines):
        print('read line ', i)
        text = json_file.readline()
        data = json.loads(text)
        with transaction.atomic():
            if len(Paper.objects.filter(pk = data['id'])) ==  1:
                continue
            paper = Paper(
                id = data['id'],
                title = data['title'],
                year = data['year']
            )
            paper.save()
            add_authors(paper, data)
            add_keywords(paper, data)
            add_fos(paper, data)
            add_venue(paper, data)
            add_n_citation(paper, data)
            add_references(paper, data)
            add_page_start(paper, data)
            add_page_end(paper, data)
            add_doc_type(paper, data)
            add_lang(paper, data)
            add_publisher(paper, data)
            add_issn(paper, data)
            add_isbn(paper, data)
            add_doi(paper, data)
            add_pdf(paper, data)
            add_url(paper, data)
            add_abstract(paper, data)
            paper.save()
    json_file.close()

def insertempty():
    s_institute = Institute.objects.filter(inst_name = 'for empty')
    if len(s_institute) == 1:
        return 
    n_institute = Institute(inst_name = 'for empty')
    n_institute.save()

if __name__ == "__main__":
    insertempty()

    data_path = '/home/elin/code/daxiangmu/mag_papers_166.txt'
    lines = 100
    main(data_path, lines)
    print('Done!')