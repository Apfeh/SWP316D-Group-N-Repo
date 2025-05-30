from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver





class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'ifpwebapp_admin'



#Policy Holder
class PolicyHolder(models.Model):
    id_number = models.CharField(primary_key=True,max_length=13)  # New Field
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    # risk 
    beneficiary_changes = models.IntegerField(default=0)
    claims_last_year = models.IntegerField(default=0)
    incomplete_documents = models.BooleanField(default=False)
    activity_timeline = models.JSONField(default=list)
    risk_score = models.FloatField(default=0.0)


    class Meta:
        db_table = 'policyholder'

#Policy 
class Policy(models.Model):#remeber to remove this
    policyId = models.AutoField(primary_key=True)
    policyHolder = models.ForeignKey(PolicyHolder, to_field="id_number", on_delete=models.CASCADE)
    policyType = models.CharField(max_length=100)
    premiumAmount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    endDate = models.DateField()



    class Meta:
        db_table = 'policy'

# Beneficiary.
class Beneficiary(models.Model):
    beneficiaryId = models.AutoField(primary_key=True)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contactNumber = models.CharField(max_length=20)
    relationshipToInsured = models.CharField(max_length=100)

    class Meta:
        db_table = 'beneficiary'

    
#Claims
class Claim(models.Model):
    claimId = models.AutoField(primary_key=True)
    policyId = models.ForeignKey(Policy, on_delete=models.CASCADE)
    beneficiaryId = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
    policyHolderId = models.ForeignKey(PolicyHolder, on_delete=models.CASCADE)
    dateFiled = models.DateField(auto_now_add=True)
    claimAmount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'claim'


#Insured Person
class InsuredPerson(models.Model):
    id = models.AutoField(primary_key=True)
    policy_id = models.ForeignKey(Policy, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    relationship_to_policy_holder = models.CharField(max_length=100)
    holder = models.ForeignKey(PolicyHolder, on_delete=models.CASCADE)

    class Meta:
        db_table = 'insuredperson'


#Fraud Team
class FraudPreventionTeam(models.Model):
    teamId = models.AutoField(primary_key=True)
    claimid = models.ForeignKey(Claim, on_delete=models.CASCADE)
    policyid = models.ForeignKey(Policy, on_delete=models.CASCADE)
    contactNumber = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    investigatorName = models.CharField(max_length=255)

    class Meta:
        db_table = 'fraudpreventionteam'


#officer
class Officer(models.Model):
    officerID = models.AutoField(primary_key=True)
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    contactNumber = models.CharField(max_length=15)
    department = models.CharField(max_length=50)
    officerName = models.CharField(max_length=100)

    def _str_(self):
        return self.officerName

class Case(models.Model):
    caseID = models.AutoField(primary_key=True)
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

    def _str_(self):
        return f"Case {self.caseID} - {self.status}"
    
    #risk assessment api
class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    policy = models.ForeignKey('Policy', on_delete=models.SET_NULL, null=True, blank=True)
    claim = models.ForeignKey('Claim', on_delete=models.SET_NULL, null=True, blank=True)
    policy_holder = models.ForeignKey('PolicyHolder', on_delete=models.SET_NULL, null=True, blank=True)
    beneficiary = models.ForeignKey('Beneficiary', on_delete=models.SET_NULL, null=True, blank=True)
    insured_person = models.ForeignKey('InsuredPerson', on_delete=models.SET_NULL, null=True, blank=True)
    fraud_team = models.ForeignKey('FraudPreventionTeam', on_delete=models.SET_NULL, null=True, blank=True)
    officer = models.ForeignKey('Officer', on_delete=models.SET_NULL, null=True, blank=True)
    case = models.ForeignKey('Case', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'notification'
        ordering = ['-created_at']

    def __str__(self):
        return self.message

class ActivityLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    details = models.TextField()

    class Meta:
        db_table = 'activity_log'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.action}"
