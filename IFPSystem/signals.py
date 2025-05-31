from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from IFPWebApp.models import Policy, Claim, PolicyHolder, Beneficiary, InsuredPerson, FraudPreventionTeam, Officer, Case, Notification

@receiver(post_save, sender=Policy)
def notify_new_policy(sender, instance, created, **kwargs):
    if created:
        message = f"New policy #{instance.policyId} created for PolicyHolder {instance.policyHolder.id_number}."
        notification = Notification.objects.create(message=message, policy=instance)
        broadcast_notification(message, notification.created_at.isoformat())

@receiver(post_save, sender=Claim)
def notify_new_claim(sender, instance, created, **kwargs):
    if created:
        message = f"New claim #{instance.claimId} filed for Policy #{instance.policyId.policyId}."
        notification = Notification.objects.create(message=message, claim=instance)
        broadcast_notification(message, notification.created_at.isoformat())

@receiver(post_save, sender=PolicyHolder)
def notify_risk_score(sender, instance, created, **kwargs):
    if not created and instance.risk_score > 80:
        message = f"Suspicious activity: PolicyHolder {instance.id_number} has risk score {instance.risk_score}."
        notification = Notification.objects.create(message=message, policy_holder=instance)
        broadcast_notification(message, notification.created_at.isoformat())

@receiver(post_save, sender=Beneficiary)
def notify_new_beneficiary(sender, instance, created, **kwargs):
    if created:
        message = f"New beneficiary {instance.name} added to Policy #{instance.policy.policyId}."
        notification = Notification.objects.create(message=message, beneficiary=instance)
        broadcast_notification(message, notification.created_at.isoformat())

@receiver(post_save, sender=InsuredPerson)
def notify_new_insured_person(sender, instance, created, **kwargs):
    if created:
        message = f"New insured person {instance.name} added to Policy #{instance.policy_id.policyId}."
        notification = Notification.objects.create(message=message, insured_person=instance)
        broadcast_notification(message, notification.created_at.isoformat())

@receiver(post_save, sender=FraudPreventionTeam)
def notify_new_fraud_team(sender, instance, created, **kwargs):
    if created:
        message = f"Fraud team assigned to Claim #{instance.claimid.claimId}."
        notification = Notification.objects.create(message=message, fraud_team=instance)
        broadcast_notification(message, notification.created_at.isoformat())

@receiver(post_save, sender=Officer)
def notify_new_officer(sender, instance, created, **kwargs):
    if created:
        message = f"New officer {instance.officerName} assigned to Claim #{instance.claim.claimId}."
        notification = Notification.objects.create(message=message, officer=instance)
        broadcast_notification(message, notification.created_at.isoformat())

@receiver(post_save, sender=Case)
def notify_new_case(sender, instance, created, **kwargs):
    if created:
        message = f"New case #{instance.caseID} created with status {instance.status}."
        notification = Notification.objects.create(message=message, case=instance)
        broadcast_notification(message, notification.created_at.isoformat())

def broadcast_notification(message, created_at):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'admin_notifications',
        {
            'type': 'send_notification',
            'message': message,
            'created_at': created_at
        }
    )