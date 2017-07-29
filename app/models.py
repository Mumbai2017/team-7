from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Sakhi(models.Model):
	user = models.OneToOneField(User)
	lat = models.CharField(max_length=100,blank=True)
	lng = models.CharField(max_length=100,blank=True)
	nachni = models.IntegerField(default=0,blank=True)
	mari = models.IntegerField(default=0,blank=True)
	oat = models.IntegerField(default=0,blank=True)

