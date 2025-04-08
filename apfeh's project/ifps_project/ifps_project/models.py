from django.db import models

class TeamMember(models.Model):
    teamid = models.AutoField(primary_key=True)
    claimid = models.IntegerField()
    policyid = models.IntegerField()
    contactNumber = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    investigatorName = models.CharField(max_length=100)

    class Meta:
        db_table = 'ifps_app_fraudpreventionteam'