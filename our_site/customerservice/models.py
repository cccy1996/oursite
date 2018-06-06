from django.db import models
from django.contrib.auth.models import User
from account.models import Expertuser_relation
from display.models import ExpertDetail

class CustomerService(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
class ApplicationForHomepageClaiming(models.Model):
    expert = models.ForeignKey(Expertuser_relation, on_delete=models.CASCADE)
    homepage = models.ForeignKey(ExpertDetail, on_delete=models.CASCADE)
    date = models.DateTimeField
    STATE_CHOICES = (
        ('P', 'Passed'),
        ('S', 'Suspending'),
        ('R', 'Rejected'),
    )
    state = models.CharField(max_length=1, choices=STATE_CHOICES)
    reject_reason = models.CharField(max_length=32)



