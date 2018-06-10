from django.db import models
from django.contrib.auth.models import User


# Study_area
# Expertuser_relation
# Commuser_relation
# Institute
# Membership


class Study_area(models.Model):
    area_name = models.CharField(max_length=30)


class Expertuser_relation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    is_register = models.BooleanField()
    Study_area = models.ManyToManyField(Study_area)
    en_name = models.CharField(max_length=50)


class Commuser_relation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    credit = models.DecimalField(max_digits=9, decimal_places=1)


class Institute(models.Model):
    inst_name = models.CharField(max_length=30)
    inst_en_name = models.CharField(max_length=45)
    inst_type = models.CharField(max_length=20)

    members = models.ManyToManyField(Expertuser_relation, through='Membership')


class Membership(models.Model):
    expert = models.ForeignKey(Expertuser_relation, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)

