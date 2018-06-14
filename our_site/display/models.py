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

def composition_appendix_path(instance, filename):
    return 'compositions/composition_{0}/appendix/{1}'.format(instance.composition.pk, filename)
def composition_display_material_path(instance, filename):
    return 'compositions/composition_{0}/display/{1}'.format(instance.composition.pk, filename)


# 关于 Appendix 和 DisplayMaterial的区别：
# Appendix 是附件，成果的说明书、论文pdf之类的东西，应该只有购买者有权下载，未购买者应该只卡看到一个列表
# DisplayMaterial 是用来展示成果效果的图片或者视频，应该所有人都能看到

class Appendix(models.Model):
    # 附件没必要保存文件类型，只要客户能下载就可以了
    composition = models.ForeignKey(Composition, on_delete = models.CASCADE)
    uploaded = models.FileField(upload_to=composition_appendix_path)

class DisplayMaterial(models.Model):
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    FILE_TYPES = (
        ('P', 'Picture'),
        ('V', 'Video'),
    )
    material_type = models.CharField(max_length=1, choices=FILE_TYPES)
    uploaded = models.FileField(upload_to=composition_display_material_path)
    description = models.CharField(max_length=32, default="")

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