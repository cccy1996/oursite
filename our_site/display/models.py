from django.db import models
from account.models import Expertuser_relation

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

def composition_directory_path(instance, filename):
    return 'composition_appendix/composition_{0}/{1}'.format(instance.composition.pk, filename)

class Appendix(models.Model):
    composition = models.ForeignKey(Composition, on_delete = models.CASCADE)
    FILE_TYPES = (
        ('T', 'Text'), # 文档一类
        ('P', 'Picture'),
        ('V', 'Video'),
    )
    app_type = models.CharField(max_length=1, choices=FILE_TYPES)
    uploaded = models.FileField(upload_to=composition_directory_path)

class ExpertDetail(models.Model):
    # a primary key defined in order to avoid repeating
    custompk = models.PositiveIntegerField(primary_key=True) 
    name = models.CharField(max_length=40)
    account = models.OneToOneField(Expertuser_relation, on_delete=models.SET_NULL, null=True)
    intro = models.CharField(max_length=512) #personal introduction
    institutes = models.ManyToManyField(Institute, through='Membership')
    study_areas = models.ManyToManyField(StudyArea)


class Membership(models.Model):
    expert = models.ForeignKey(ExpertDetail, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    post = models.CharField(max_length=50) #职务 