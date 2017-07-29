from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Sakhi(models.Model):
	user = models.OneToOneField(User)
	phone = models.CharField(max_length=100,blank=True)
	lat = models.CharField(max_length=100,blank=True)
	lng = models.CharField(max_length=100,blank=True)
	nachni = models.IntegerField(default=0,blank=True)
	mari = models.IntegerField(default=0,blank=True)
	oat = models.IntegerField(default=0,blank=True)
class Customer(models.Model):
	user = models.OneToOneField(User)
	phone = models.CharField(max_length=100,blank=True)
	lat = models.CharField(max_length=100,blank=True)
	lng = models.CharField(max_length=100,blank=True)
	pending_order_id = models.IntegerField(default=0)

class Gruh(models.Model):
	nachni = models.IntegerField(default=0)
	mari = models.IntegerField(default=0)
	oat = models.IntegerField(default=0)
class Order(models.Model):
	placed_by = models.IntegerField()
	placed_from = models.IntegerField()
	nachni = models.IntegerField(default=0)
	mari = models.IntegerField(default=0)
	oat = models.IntegerField(default=0)

