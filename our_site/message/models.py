from django.db import models
from django.contrib.auth.models import User


class Inbox(models.Model):
    inbox_id = models.AutoField(primary_key=True)
    inbox_date = models.DateTimeField('inbox message date')
    inbox_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_sends")
    inbox_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_receive")
    inbox_content = models.CharField(max_length=255)
