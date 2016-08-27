from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    startTime = models.DateField(auto_now=False, auto_now_add=False)
    endTime = models.DateField(auto_now=False, auto_now_add=False)
    ownerName = models.CharField(max_length=100)

