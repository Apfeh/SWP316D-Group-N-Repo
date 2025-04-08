from django.db import models

class InsuredPerson(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    policy_id = models.BigIntegerField()
    date_of_birth = models.CharField(max_length=100)
    consent_verified = models.IntegerField()
    relationship_to_policy_holder = models.CharField(max_length=20)

    class Meta:
        db_table = 'ifps_app_insuredperson'
