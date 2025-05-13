# IFPWebApp/models.py
from django.db import models

class PolicyHolder(models.Model):
    idno = models.CharField(max_length=50, primary_key=True)  # e.g., national ID number
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.idno})"

class Policy(models.Model):
    policyID = models.AutoField(primary_key=True)
    policyHolder = models.ForeignKey(PolicyHolder, on_delete=models.CASCADE, to_field='idno')
    policyType = models.CharField(max_length=100)
    premiumAmount = models.DecimalField(max_digits=10, decimal_places=2)
    startDate = models.DateField()
    endDate = models.DateField()

    def get_formal_policy_type(self):
        """Return a formalized version of policyType."""
        type_map = {
            'life': 'Life Insurance',
            'health': 'Health Insurance',
            'auto': 'Auto Insurance',
            # Add other policy types as needed
        }
        return type_map.get(self.policyType.lower(), self.policyType.title())

    def __str__(self):
        return f"Policy {self.policyID} - {self.policyType}"

class InsuredPerson(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dateOfBirth = models.DateField()
    relationshipToPolicyHolder = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Beneficiary(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contactNumber = models.CharField(max_length=50)
    relationshipToInsured = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Claim(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
    claimAmount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Claim for Policy {self.policy.policyID}"