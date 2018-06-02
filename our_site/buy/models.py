from django.db import models
from account.models import Commuser_relation
from display.models import Composition

# Create your models here.
class Transaction(models.Model):
    trans_id = models.AutoField(primary_key=True)
    trans_date = models.DateTimeField('transaction occured date')
    trans_user = models.ForeignKey(Commuser_relation, on_delete = False)
    trans_composition = models.ForeignKey(Composition, on_delete = False)
    trans_price = models.DecimalField(max_digits=9,decimal_places=1)