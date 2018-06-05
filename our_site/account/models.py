from django.db import models
from django.contrib.auth.models import User

class Study_area(models.Model):
    area_name = models.CharField(max_length=30)

class Expertuser_relation(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    name = models.CharField(max_length=40)
    identity = models.CharField(max_length=18)

class Commuser_relation(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    credit = models.DecimalField(max_digits=9,decimal_places=1)


