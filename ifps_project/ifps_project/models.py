from django.db import models

class Admin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

class PolicyHolder(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

