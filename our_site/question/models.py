from django.db import models
from account.models import Commuser_relation, Expertuser_relation


class Question(models.Model):
    que_id = models.AutoField(primary_key=True)
    que_title = models.CharField(max_length=30)
    que_content = models.CharField(max_length=500)
    que_date = models.DateTimeField('question occured date', auto_now=True)
    que_price = models.IntegerField(default=0)
    ans_status = models.BooleanField(default=False)
    ans_content = models.CharField(max_length=500, null=True, blank=True)
    ans_date = models.DateTimeField('answered date', null=True, blank=True)

    que_user = models.ForeignKey(Commuser_relation,
                                 on_delete=models.CASCADE,
                                 related_name="commuser_question")
    ans_expert = models.ForeignKey(Expertuser_relation,
                                   on_delete=models.CASCADE,
                                   related_name="expert_answer", null=True, blank=True)

    def que_info(self):
        return {'que_id': self.que_id,
                'que_title': self.que_title,
                'que_date': self.que_date,
                'que_content': self.que_content,
                }