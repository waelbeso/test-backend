# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid



#"id": "xxx",                  // user id(you can use uuid or the id provided by database, but need to be unique)
#"name": "test",               // user name
#"dob": "",                    // date of birth
#"address": "",                // user address
#"description": "",            // user description
#"created_at": ""              // user created date

class User(AbstractUser):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	dob = models.DateField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return str(self.username)

	@property
	def created_at(self):
		return self.date_joined

class Address (models.Model):
	id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user      = models.ForeignKey("User",related_name='address', on_delete=models.CASCADE)
	name      = models.CharField(max_length=55,null=True,blank=True)
	country   = models.CharField(max_length=13,null=True,blank=True)
	province  = models.CharField(max_length=55,null=True,blank=True)
	city      = models.CharField(max_length=55,null=True,blank=True)
	zip_code  = models.CharField(max_length=20,null=True,blank=True)
	address   = models.CharField(max_length=250,null=True,blank=True)

	class Meta:
		unique_together = (("user", "name"),)

	def __unicode__(self): 
		return '{} <{}>'.format(self.name, self.user)


