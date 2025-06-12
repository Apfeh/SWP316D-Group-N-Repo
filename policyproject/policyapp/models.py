from django.db import models
from django.conf import settings

# Create your models here.
class PolicyHolder(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='policyholder'
    )
    id_number = models.CharField(primary_key=True, max_length=20)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    beneficiary_changes = models.IntegerField(default=0)
    claims_last_year = models.IntegerField(default=0)
    incomplete_documents = models.BooleanField(default=False)
    activity_timeline = models.JSONField(default=list)
    risk_score = models.FloatField(default=0.0)
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