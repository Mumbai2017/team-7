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
	def __str__(self):
		return str(self.user.username)
class Customer(models.Model):
	user = models.OneToOneField(User)
	phone = models.CharField(max_length=100,blank=True)
	lat = models.CharField(max_length=100,blank=True)
	lng = models.CharField(max_length=100,blank=True)
	pending_order_id = models.IntegerField(default=0)
	def __str__(self):
		return str(self.user.username)
class Gruh(models.Model):
	nachni = models.IntegerField(default=0)
	mari = models.IntegerField(default=0)
	oat = models.IntegerField(default=0)
class Order(models.Model):
	placed_by = models.IntegerField()
	placed_from = models.IntegerField(blank=True,null=True)
	nachni = models.IntegerField(default=0)
	mari = models.IntegerField(default=0)
	oat = models.IntegerField(default=0)
	urgent = models.IntegerField(default=-1)
	order_direction = models.IntegerField(default=-1)
	def __str__(self):
		return str(self.id)
class Distance(models.Model):
	sakhi_id = models.IntegerField()
	customer_id = models.IntegerField()
	distance = models.IntegerField(default=5000000)
	customer_addr = models.CharField(max_length=500)
	sakhi_addr = models.CharField(max_length=500)
	sakhi_lng = models.CharField(max_length=100,blank=True)
	sakhi_lat = models.CharField(max_length=100,blank=True)
	customer_lat = models.CharField(max_length=100,blank=True)
	customer_lng = models.CharField(max_length=100,blank=True)
