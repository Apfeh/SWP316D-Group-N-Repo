from django.db import models

# Beneficiary.
class Beneficiary(models.Model):
    beneficiaryId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contactNumber = models.CharField(max_length=20)
    relationshipToInsured = models.CharField(max_length=50)
    policy_number =0#add foreing key policy number

    def __str__(self):
        return self.name
    
    #Claims
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


#Insured Person
class InsuredPerson(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    policy_id = models.BigIntegerField()
    date_of_birth = models.CharField(max_length=100)
    consent_verified = models.IntegerField()
    relationship_to_policy_holder = models.CharField(max_length=20)

    class Meta:
        db_table = 'ifps_app_insuredperson'

#Policy Holder

class PolicyHolder(models.Model):
    policyHolderId = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=15)
    email = models.EmailField()

    class Meta:
        db_table = 'policyholder'

#Fraud Team
class TeamMember(models.Model):
    teamid = models.AutoField(primary_key=True)
    claimid = models.IntegerField()
    policyid = models.IntegerField()
    contactNumber = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    investigatorName = models.CharField(max_length=100)

    class Meta:
        db_table = 'ifps_app_fraudpreventionteam'