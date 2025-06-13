from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings




# models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Database router first
class HomeAffairsRouter:
    """
    Routes Home Affairs models to homeaffairsdb
    """
    ha_models = {
        'citizen', 'address', 'document', 'birthcertificate',
        'deathcertificate', 'passport', 'photo', 'marriage',
        'marriageparticipant'
    }

    def db_for_read(self, model, **hints):
        if model._meta.model_name in self.ha_models:
            return 'homeaffairs'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        if {obj1._meta.model_name, obj2._meta.model_name} <= self.ha_models:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'homeaffairs':
            return False  # Never migrate homeaffairs database
        elif db == 'default':
            return model_name not in self.ha_models  # Only migrate non-HA models
        return None

# IFPS Models (managed by Django)
class Admin(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_profile'
    )
    
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    class Meta:
        db_table = 'ifpwebapp_admin'

class PolicyHolder(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='policyholder'
    )
    id_number = models.CharField(primary_key=True, max_length=20)
    phone_number = models.CharField(max_length=15, blank=True)
    name = models.CharField(max_length=200)
    beneficiary_changes = models.IntegerField(default=0)
    claims_last_year = models.IntegerField(default=0)
    incomplete_documents = models.BooleanField(default=False)
    activity_timeline = models.JSONField(default=list)
    risk_score = models.FloatField(default=0.0)
    email = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table = 'policyholder'

#Policy 
class Policy(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ]
    
    policyId = models.AutoField(primary_key=True)
    policyHolder = models.ForeignKey('PolicyHolder', on_delete=models.CASCADE)
    policyType = models.CharField(max_length=50)
    premiumAmount = models.DecimalField(max_digits=10, decimal_places=2)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()  # 7 days from creation

    class Meta:
        db_table = 'policy'

    def get_formal_policy_type(self):
        return "Life Insurance" if self.policyType == "life" else "Funeral Insurance"


# Beneficiary.
class Beneficiary(models.Model):
    beneficiaryId = models.AutoField(primary_key=True)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contactNumber = models.CharField(max_length=100)
    relationshipToInsured = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=255) #create this column using sql
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
    holder = models.ForeignKey('PolicyHolder', on_delete=models.CASCADE)
    id_number = models.CharField(max_length=20)
    parent_id_number = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True, null=True)

    STATUS_CHOICES = [
        ('alive', 'Alive'),
        ('deceased', 'Deceased'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='alive'
    )

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

# Home Affairs Models (read-only)
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

    class Meta:
        managed = False
        db_table = 'citizen'

class Address(models.Model):
    addressId = models.AutoField(primary_key=True)
    idNumber = models.ForeignKey(Citizen, on_delete=models.DO_NOTHING, db_column='idNumber')
    streetAddress = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postalCode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15, blank=True)

    class Meta:
        managed = False
        db_table = 'address'

    


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

    class Meta:
        managed = False
        db_table = 'citizen'
        app_label = 'IFPWebApp'

class Address(models.Model):
    addressId = models.AutoField(primary_key=True)
    idNumber = models.ForeignKey(Citizen, on_delete=models.CASCADE, db_column='idNumber')
    streetAddress = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postalCode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15, blank=True)

    class Meta:
        managed = False
        db_table = 'address'

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



# verification/models.py
from django.db import models
from django.utils import timezone
import random

from django.utils import timezone

class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)

    def is_expired(self):
        return timezone.now() > self.expires_at

    class Meta:
        db_table = 'otp'

class PendingBeneficiary(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    relationship = models.CharField(max_length=100)
    token = models.CharField(max_length=36, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pending_beneficiary'

import uuid
class ApprovalRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    insured_person = models.ForeignKey(InsuredPerson, on_delete=models.CASCADE, null=True, blank=True)
    policy_data = models.JSONField()  # Store policy data until approval
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notification_sent = models.BooleanField(default=False)

    class Meta:
        db_table = 'approval_request'

class Notification(models.Model):
    TYPE_CHOICES = [
        ('approval_sent', 'Approval Sent'),
        ('approval_received', 'Approval Received'),
        ('policy_active', 'Policy Activated'),
        ('claim', 'Claim Notification'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    related_policy = models.ForeignKey(Policy, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'notification'
        ordering = ['-created_at']

class Admin_notification(models.Model):
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
        db_table = 'admin_notifications'
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