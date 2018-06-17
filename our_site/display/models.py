from django.db import models
from account.models import Expertuser_relation

<<<<<<< HEAD
=======
class Institute(models.Model):
    inst_name = models.CharField(max_length=30)
    inst_en_name = models.CharField(max_length=45)
    inst_type = models.CharField(max_length=20)

class StudyArea(models.Model):
    area_name = models.CharField(max_length=30) 

class Composition(models.Model):
    comp_name = models.CharField(max_length=50)
    upload_time = models.DateTimeField('composition uploaded time')
    expert = models.ForeignKey(Expertuser_relation, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9,decimal_places=1, default = 0)
    description = models.CharField(max_length=500) # 一个总体性的说明

class Project(models.Model):
    composition = models.OneToOneField(Composition, on_delete = models.CASCADE, primary_key = True)
    organization = models.CharField(max_length=25)
    start_time = models.DateTimeField('project started time')
    end_time = models.DateTimeField('project ended time')
    
class Paper(models.Model):
    composition = models.OneToOneField(Composition, on_delete = models.CASCADE, primary_key = True)
    abstract = models.CharField(max_length=200)
    keywords = models.CharField(max_length=40) # 应规定一个格式，如用分号将各个关键词隔开之类

class Patent(models.Model):
    composition = models.OneToOneField(Composition, on_delete = models.CASCADE, primary_key = True)
    patent_no = models.CharField(max_length=15)
    apply_time = models.DateTimeField('patent applied time')
    auth_time = models.DateTimeField('patent authorized time')
>>>>>>> c5c17c47fa891cac7c7c1bbb6e28289fe7d5471a

class Keyword(models.Model):
    word = models.CharField(max_length=100)


class StudyArea(models.Model):
    Area_name = models.CharField(max_length=255)

class Institute(models.Model):
    inst_name = models.CharField(max_length=255)


class ExpertDetail(models.Model):
    # a primary key defined in order to avoid repeating
    custompk = models.AutoField(primary_key = True)
    name = models.CharField(max_length=100) #find a name length 68!
    account = models.OneToOneField(Expertuser_relation, on_delete=models.SET_NULL, null=True)
    institute = models.ForeignKey(Institute, related_name="members", on_delete = models.SET_NULL, null = True)
    class Meta:
        unique_together=('name', 'institute')

class Paper(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    title = models.CharField(max_length=512)
    authors = models.ManyToManyField(ExpertDetail, related_name="papers")
    venue = models.TextField(null=True)
    year = models.IntegerField()
    keywords = models.ManyToManyField(Keyword, related_name='related_paper')
    fos = models.ManyToManyField(StudyArea, related_name='related_paper')
    n_citation = models.IntegerField(null=True)
    references = models.TextField(null=True)
    page_start = models.IntegerField(null=True)
    page_end = models.IntegerField(null=True)
    doc_type = models.CharField(max_length=20, null=True)
    lang = models.CharField(max_length=20, null=True)
    publisher = models.CharField(max_length=255, null=True)
    issn = models.CharField(max_length=30, null=True)
    isbn = models.CharField(max_length=30, null=True)
    doi = models.CharField(max_length=50, null=True)
    pdf = models.TextField(null=True)
    url = models.TextField(null=True)
    abstract = models.TextField(null=True)
