from django.db import models
'''
from account.models import Commuser_relation
from display.models import Paper

# Create your models here.


class Transaction(models.Model):
    trans_id = models.AutoField(primary_key=True)
    app_date = models.DateTimeField('application occured date')
    trans_date = models.DateTimeField(
        'transaction occured date', null=True, blank=True)
    trans_user = models.ForeignKey(Commuser_relation, on_delete=False)
    trans_composition = models.ForeignKey(Paper, on_delete=False)
    trans_price = models.DecimalField(max_digits=9, decimal_places=1)
    is_accept = models.NullBooleanField()
    is_paid = models.NullBooleanField()
'''
