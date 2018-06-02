from django.db import models
from account.models import Commuser_relation, Expertuser_realtion

class Question(models.Model):
    que_id = models.AutoField(primary_key=True)
    que_content = models.CharField(max_length=500)
    que_date = models.DateTimeField('question occured date')
    ans_content = models.CharField(max_length=500)
    ans_date = models.DateTimeField('answered date')

    que_user = models.ForeignKey(Commuser_relation, on_delete = models.CASCADE, related_name="commuser_question")
    ans_expert = models.ForeignKey(Expertuser_realtion, on_delete = models.CASCADE, related_name="expert_answer")
