import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "our_site.settings") 
import django
django.setup()

from display.models import *
from django.db import transaction
import json
import chunksgen

class TooLongException(Exception):
    def __init__(self, err='item too long, skip it'):
        Exception.__init__(self, err)

def add_authors(paper, data):
    for author in data['authors']:
        if 'org' in author:
            if len(author['org']) > 255:
                raise TooLongException()
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
            empty_institute = Institute.objects.get(pk = 1)
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
        if len(keyword) > 100:
            raise TooLongException()    
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
        if len(field) > 255:
            raise TooLongException()
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
    if len(data['doc_type']) > 20:
        raise TooLongException()
    paper.doc_type = data['doc_type']
def add_lang(paper, data):
    if 'lang' not in data:
        return
    if len(data['lang']) > 20:
        raise TooLongException()
    paper.lang = data['lang']
def add_publisher(paper, data):
    if 'publisher' not in data:
        return
    if len(data['publisher']) > 255:
        raise TooLongException()
    paper.publisher = data['publisher']
def add_issn(paper, data):
    if 'issn' not in data:
        return
    if len(data['issn']) > 30:
        raise TooLongException()
    paper.issn = data['issn']
def add_isbn(paper, data):
    if 'isbn' not in data:
        return
    if len(data['isbn']) > 30:
        raise TooLongException()
    paper.isbn = data['isbn']
def add_doi(paper, data):
    if 'doi' not in data:
        return
    if len(data['doi']) > 50:
        raise TooLongException()
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
        # 舍弃有不正常关键字的对象
        if 'keywords' in data:
            if len(data['keywords'][0]) > 100:
                continue
        
        try:
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
        except TooLongException:
            pass #跳过这行json
    json_file.close()



if __name__ == "__main__":
    # 添加一个pk为1的空institute
    try:
        insts = Institute.objects.get(pk=1)
    except Institute.DoesNotExist:
        Institute.objects.create(
            inst_name='empty_institute'
        )
    data_path = '/home/shiletong/mag_papers_8/mag_papers_166.txt'
    main(data_path, 1000)
    printf('Begin to generate chunks for titles...')
    chunksgen.gen_for_all()
    print('Done!')