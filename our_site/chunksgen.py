import nltk
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "our_site.settings")
import django
django.setup()
from display.models import *
from django.db.utils import *
from search.models import *

def make_parser():
    tag_pattern = "CHUNK: {<DT>?<JJ.*>*<NN.*>+(<IN><DT>?<JJ.*>*<NN.*>)?}"
    return nltk.RegexpParser(tag_pattern)

def chunks_from_title(title, parser):
    tokens = nltk.word_tokenize(title)
    tagged_tokens = nltk.pos_tag(tokens)
    tree = parser.parse(tagged_tokens)
    s = set()
    for t in tree.subtrees(lambda s: s.label() == 'CHUNK'):
        words = [w[0] for w in t.leaves()]
        chunk = ' '.join(words)
        if len(chunk) <= 64:
            s.add(chunk)
    return s

# for debug
def print_all():
    parser = make_parser()
    for paper in Paper.objects.all():
        s = chunks_from_title(paper.title, parser)
        print(s)

def gen_for_all():
    parser = make_parser()
    for paper in Paper.objects.all():
        s = chunks_from_title(paper.title, parser)
        for c in s:
            try:
                ChunkFromTitle.objects.create(chunk=c, paper=paper)
            except IntegrityError:
                pass

if __name__ == '__main__':
    gen_for_all()