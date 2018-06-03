from django.db import models
from account.models import Expertuser_relation

class Composition(models.Model):
    comp_id = models.AutoField(primary_key=True)
    comp_name = models.CharField(max_length=50)
    upload_time = models.DateTimeField('composition uploaded time')
    expert = models.ForeignKey(Expertuser_relation, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9,decimal_places=1, default = 0)

class Project(Composition):
    composition = models.OneToOneField(Composition, on_delete = models.CASCADE, primary_key = True)
    proj_type = models.CharField(max_length=25)
    organization = models.CharField(max_length=25)
    expense = models.IntegerField()
    start_time = models.DateTimeField('project started time')
    end_time = models.DateTimeField('project ended time')

class Paper(Composition):
    composition = models.OneToOneField(Composition, on_delete = models.CASCADE, primary_key = True)
    origin = models.CharField(max_length=25)
    abstractt = models.CharField(max_length=200)
    keyword = models.CharField(max_length=40)

class Patent(Composition):
    composition = models.OneToOneField(Composition, on_delete = models.CASCADE, primary_key = True)
    patent_type = models.CharField(max_length=25)
    patent_no = models.CharField(max_length=25)
    apply_time = models.DateTimeField('patent applied time')
    auth_time = models.DateTimeField('patent authorized time')

def composition_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'composition_{0}/{1}'.format(instance.composition.comp_id, filename)

class Appendix(models.Model):
    #composition = models.CharField(max_length=50)
    app_id = models.AutoField(primary_key=True)
    composition = models.ForeignKey(Composition, on_delete = models.CASCADE)
    app_type = models.CharField(max_length=10)
    upload_time = models.DateTimeField('uploaded time')
    upload_path = models.FileField(upload_to=composition_directory_path)
    upload_size = models.DecimalField(max_digits=8,decimal_places=2)
