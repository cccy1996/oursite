from django.db import models
from display.models import *

class ChunkFromTitle(models.Model):
    chunk = models.CharField(max_length=64, primary_key=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)

 