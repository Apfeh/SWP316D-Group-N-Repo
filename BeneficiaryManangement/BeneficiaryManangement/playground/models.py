from django.db import models

# Create your models here.
class Beneficiary(models.Model):
    beneficiaryId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contactNumber = models.CharField(max_length=10)
    relationshipToInsured = models.CharField(max_length=50)

    def _str_(self):
        return self.name