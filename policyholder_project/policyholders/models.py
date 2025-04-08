from django.db import models

# Create your models here.

class PolicyHolder(models.Model):
    policyHolderId = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=15)
    email = models.EmailField()

    class Meta:
        db_table = 'policyholder'

