from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .fraud_detection import run_automatic_checks





#Policy Holder
class PolicyHolder(models.Model):
    id_number = models.CharField(primary_key=True,max_length=13)  # New Field
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    email = models.EmailField(unique=True)  # Used as username
    password = models.CharField(max_length=128)

    class Meta:
        db_table = 'policyholder'

#Policy 
class Policy(models.Model):#remeber to remove this
    policyId = models.AutoField(primary_key=True)
    policyHolder = models.ForeignKey(PolicyHolder, to_field="id_number", on_delete=models.CASCADE)
    policyType = models.CharField(max_length=100)
    premiumAmount = models.DecimalField(max_digits=10, decimal_places=2)
    startDate = models.DateField()
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


from django.utils import timezone

# Suspicious activities detected by the system
class SuspiciousActivity(models.Model):
    policyHolder = models.ForeignKey(PolicyHolder, on_delete=models.CASCADE)
    description = models.TextField()
    detected_at = models.DateTimeField(default=timezone.now)
    resolved = models.BooleanField(default=False)

    class Meta:
        db_table = 'suspicious_activity'

    def __str__(self):
        return f"SuspiciousActivity for {self.policyHolder.name} at {self.detected_at}"


# Risk score for a policyholder after assessment
class RiskAssessment(models.Model):
    policyHolder = models.ForeignKey(PolicyHolder, on_delete=models.CASCADE)
    risk_score = models.IntegerField()
    requires_manual_approval = models.BooleanField(default=False)
    assessed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'risk_assessment'

    def __str__(self):
        return f"RiskAssessment: {self.policyHolder.name} = {self.risk_score}"


@receiver(post_save, sender=Policy)
def auto_check_fraud(sender, instance, created, **kwargs):
    if created:
        run_automatic_checks(instance.policyHolder)



# home affairs database

# models.py
from django.db import models

class Citizen(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    idNumber = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    dateOfBirth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    homeLanguage = models.CharField(max_length=100, blank=True, null=True)
     

    def __str__(self):
        return f"{self.name} {self.surname} ({self.idNumber})"
    class Meta:
        app_label = 'IFPWebApp'
        db_table = 'citizen'  
class Address(models.Model):
    addressId = models.AutoField(primary_key=True)
    idNumber = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    streetAddress = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postalCode = models.CharField(max_length=10)

class Document(models.Model):
    documentId = models.AutoField(primary_key=True)
    idNumber = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    documentType = models.CharField(max_length=100)
    issueDate = models.DateField()
    expiryDate = models.DateField(blank=True, null=True)
    documentStatus = models.CharField(max_length=50)

class BirthCertificate(models.Model):
    birthCertId = models.AutoField(primary_key=True)
    idNumber = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    placeOfBirth = models.CharField(max_length=100)
    birthDate = models.DateField()
    registeredBy = models.CharField(max_length=100)
    registrationDate = models.DateField()

class DeathCertificate(models.Model):
    deathCertId = models.AutoField(primary_key=True)
    idNumber = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    deathDate = models.DateField()
    causeOfDeath = models.CharField(max_length=255)
    placeOfDeath = models.CharField(max_length=100)

class Passport(models.Model):
    passportId = models.AutoField(primary_key=True)
    idNumber = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    issueDate = models.DateField()
    expiryDate = models.DateField()
    countryOfIssue = models.CharField(max_length=100)

class Photo(models.Model):
    photoId = models.AutoField(primary_key=True)
    idNumber = models.ForeignKey(Citizen, on_delete=models.CASCADE, db_column='idNumber')
    imageData = models.BinaryField()
    uploadDate = models.DateField(auto_now_add=True)
    class Meta:
        app_label = 'IFPWebApp'
        db_table = 'photo'
class Marriage(models.Model):
    marriageId = models.AutoField(primary_key=True)
    marriageDate = models.DateField()
    marriageStatus = models.CharField(max_length=50)
    marriageType = models.CharField(max_length=50)

class MarriageParticipant(models.Model):
    participantId = models.AutoField(primary_key=True)
    marriageId = models.ForeignKey(Marriage, on_delete=models.CASCADE)
    citizenId = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    marriageType = models.CharField(max_length=50)