from __future__ import unicode_literals

from django.db import models

# Create your models here.

class FeedRss(models.Model):
	titulo = models.CharField(max_length=200)
	enlace = models.CharField(max_length=200)
	descripcion = models.CharField(max_length=200)