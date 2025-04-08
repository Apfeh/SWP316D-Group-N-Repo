# claim/models.py
from django.db import models

class Claim(models.Model):
    claimId = models.AutoField(primary_key=True)
    policyId = models.IntegerField()
    beneficiaryId = models.IntegerField()
    policyHolderId = models.IntegerField()
    dateFiled = models.DateField(auto_now_add=True)
    claimAmount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"Claim {self.claimId} - Policy {self.policyId}"
