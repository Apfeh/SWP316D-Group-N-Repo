# IFPWebApp/signals.py
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from IFPWebApp.models import (
    PolicyHolder, Policy, Beneficiary, Claim, InsuredPerson, FraudPreventionTeam,
    Officer, Case, PendingBeneficiary, ApprovalRequest, Notification, Admin_notification
)
import logging

# Set up logging
logger = logging.getLogger(__name__)
print("Loading signals.py")  # Debug

def broadcast_notification(message, created_at, notification_id):
    """Broadcast notification to WebSocket group."""
    try:
        logger.info(f"Broadcasting notification: {message} (ID: {notification_id})")
        channel_layer = get_channel_layer()
        if channel_layer is None:
            logger.error("Channel layer is not configured")
            return
        async_to_sync(channel_layer.group_send)(
            'admin_notifications',
            {
                'type': 'send_notification',
                'message': message,
                'created_at': created_at,
                'id': notification_id
            }
        )
    except Exception as e:
        logger.error(f"Error in broadcast_notification: {e}")

# Store previous state for update detection
previous_instances = {}

@receiver(pre_save, sender=PolicyHolder)
@receiver(pre_save, sender=Policy)
@receiver(pre_save, sender=Beneficiary)
@receiver(pre_save, sender=Claim)
@receiver(pre_save, sender=InsuredPerson)
@receiver(pre_save, sender=FraudPreventionTeam)
@receiver(pre_save, sender=Officer)
@receiver(pre_save, sender=Case)
@receiver(pre_save, sender=PendingBeneficiary)
@receiver(pre_save, sender=ApprovalRequest)
@receiver(pre_save, sender=Notification)
def store_previous_instance(sender, instance, **kwargs):
    """Store instance state before save for update detection."""
    if instance.pk:
        try:
            previous_instances[(sender, instance.pk)] = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            pass

@receiver(post_save, sender=PolicyHolder)
def notify_policy_holder(sender, instance, created, **kwargs):
    """Handle PolicyHolder create/update."""
    if created:
        message = f"New PolicyHolder created: {instance.name} (ID: {instance.id_number})"
        logger.info(f"Creating notification: {message}")
        notification = Admin_notification.objects.create(
            message=message,
            policy_holder=instance
        )
        broadcast_notification(message, notification.created_at.isoformat(), notification.id)
    else:
        previous = previous_instances.pop((sender, instance.pk), None)
        if previous:
            changes = []
            if previous.name != instance.name:
                changes.append(f"Name changed from '{previous.name}' to '{instance.name}'")
            if previous.risk_score != instance.risk_score:
                changes.append(f"Risk score changed from {previous.risk_score} to {instance.risk_score}")
            if changes:
                message = f"PolicyHolder updated (ID: {instance.id_number}): {'; '.join(changes)}"
                logger.info(f"Creating notification: {message}")
                notification = Admin_notification.objects.create(
                    message=message,
                    policy_holder=instance
                )
                broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_delete, sender=PolicyHolder)
def notify_policy_holder_delete(sender, instance, **kwargs):
    """Handle PolicyHolder deletion."""
    message = f"PolicyHolder deleted: {instance.name} (ID: {instance.id_number})"
    logger.info(f"Creating notification: {message}")
    notification = Admin_notification.objects.create(message=message)
    broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_save, sender=Policy)
def notify_policy(sender, instance, created, **kwargs):
    """Handle Policy create/update."""
    if created:
        message = f"New Policy created: #{instance.policyId} for {instance.policyHolder.name}"
        logger.info(f"Creating notification: {message}")
        notification = Admin_notification.objects.create(
            message=message,
            policy=instance
        )
        broadcast_notification(message, notification.created_at.isoformat(), notification.id)
    else:
        previous = previous_instances.pop((sender, instance.pk), None)
        if previous:
            changes = []
            if previous.status != instance.status:
                changes.append(f"Status changed from '{previous.status}' to '{instance.status}'")
            if previous.premiumAmount != instance.premiumAmount:
                changes.append(f"Premium changed from {previous.premiumAmount} to {instance.premiumAmount}")
            if changes:
                message = f"Policy updated (#{instance.policyId}): {'; '.join(changes)}"
                logger.info(f"Creating notification: {message}")
                notification = Admin_notification.objects.create(
                    message=message,
                    policy=instance
                )
                broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_delete, sender=Policy)
def notify_policy_delete(sender, instance, **kwargs):
    """Handle Policy deletion."""
    message = f"Policy deleted: #{instance.policyId}"
    logger.info(f"Creating notification: {message}")
    notification = Admin_notification.objects.create(message=message)
    broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_save, sender=Beneficiary)
def notify_beneficiary(sender, instance, created, **kwargs):
    """Handle Beneficiary create/update."""
    if created:
        message = f"New Beneficiary added to Policy #{instance.policy.policyId}: {instance.name}"
        logger.info(f"Creating notification: {message}")
        notification = Admin_notification.objects.create(
            message=message,
            beneficiary=instance
        )
        broadcast_notification(message, notification.created_at.isoformat(), notification.id)
    else:
        previous = previous_instances.pop((sender, instance.pk), None)
        if previous:
            changes = []
            if previous.name != instance.name:
                changes.append(f"Name changed from '{previous.name}' to '{instance.name}'")
            if previous.relationshipToInsured != instance.relationshipToInsured:
                changes.append(f"Relationship changed from '{previous.relationshipToInsured}' to '{instance.relationshipToInsured}'")
            if changes:
                message = f"Beneficiary updated (Policy #{instance.policy.policyId}): {'; '.join(changes)}"
                logger.info(f"Creating notification: {message}")
                notification = Admin_notification.objects.create(
                    message=message,
                    beneficiary=instance
                )
                broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_delete, sender=Beneficiary)
def notify_beneficiary_delete(sender, instance, **kwargs):
    """Handle Beneficiary deletion."""
    message = f"Beneficiary deleted from Policy #{instance.policy.policyId}: {instance.name}"
    logger.info(f"Creating notification: {message}")
    notification = Admin_notification.objects.create(message=message)
    broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_save, sender=Claim)
def notify_claim(sender, instance, created, **kwargs):
    """Handle Claim create/update."""
    if created:
        message = f"New Claim filed: #{instance.claimId} for Policy #{instance.policyId.policyId}"
        logger.info(f"Creating notification: {message}")
        notification = Admin_notification.objects.create(
            message=message,
            claim=instance
        )
        broadcast_notification(message, notification.created_at.isoformat(), notification.id)
    else:
        previous = previous_instances.pop((sender, instance.pk), None)
        if previous:
            changes = []
            if previous.status != instance.status:
                changes.append(f"Status changed from '{previous.status}' to '{instance.status}'")
            if previous.claimAmount != instance.claimAmount:
                changes.append(f"Amount changed from {previous.claimAmount} to {instance.claimAmount}")
            if changes:
                message = f"Claim updated (#{instance.claimId}): {'; '.join(changes)}"
                logger.info(f"Creating notification: {message}")
                notification = Admin_notification.objects.create(
                    message=message,
                    claim=instance
                )
                broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_delete, sender=Claim)
def notify_claim_delete(sender, instance, **kwargs):
    """Handle Claim deletion."""
    message = f"Claim deleted: #{instance.claimId}"
    logger.info(f"Creating notification: {message}")
    notification = Admin_notification.objects.create(message=message)
    broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_save, sender=InsuredPerson)
def notify_insured_person(sender, instance, created, **kwargs):
    """Handle InsuredPerson create/update."""
    if created:
        policy_id = instance.policy_id.policyId if instance.policy_id else "Unknown"
        message = f"New InsuredPerson added to Policy #{policy_id}: {instance.name}"
        logger.info(f"Creating notification: {message}")
        notification = Admin_notification.objects.create(
            message=message,
            insured_person=instance
        )
        broadcast_notification(message, notification.created_at.isoformat(), notification.id)
    else:
        previous = previous_instances.pop((sender, instance.pk), None)
        if previous:
            changes = []
            if previous.name != instance.name:
                changes.append(f"Name changed from '{previous.name}' to '{instance.name}'")
            if previous.status != instance.status:
                changes.append(f"Status changed from '{previous.status}' to '{instance.status}'")
            if changes:
                policy_id = instance.policy_id.policyId if instance.policy_id else "Unknown"
                message = f"InsuredPerson updated (Policy #{policy_id}): {'; '.join(changes)}"
                logger.info(f"Creating notification: {message}")
                notification = Admin_notification.objects.create(
                    message=message,
                    insured_person=instance
                )
                broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_delete, sender=InsuredPerson)
def notify_insured_person_delete(sender, instance, **kwargs):
    """Handle InsuredPerson deletion."""
    policy_id = instance.policy_id.policyId if instance.policy_id else "Unknown"
    message = f"InsuredPerson deleted from Policy #{policy_id}: {instance.name}"
    logger.info(f"Creating notification: {message}")
    notification = Admin_notification.objects.create(message=message)
    broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_save, sender=FraudPreventionTeam)
def notify_fraud_team(sender, instance, created, **kwargs):
    """Handle FraudPreventionTeam create/update."""
    if created:
        message = f"New FraudPreventionTeam assigned to Claim #{instance.claimid.claimId}: {instance.investigatorName}"
        logger.info(f"Creating notification: {message}")
        notification = Admin_notification.objects.create(
            message=message,
            fraud_team=instance
        )
        broadcast_notification(message, notification.created_at.isoformat(), notification.id)
    else:
        previous = previous_instances.pop((sender, instance.pk), None)
        if previous:
            changes = []
            if previous.investigatorName != instance.investigatorName:
                changes.append(f"Investigator changed from '{previous.investigatorName}' to '{instance.investigatorName}'")
            if changes:
                message = f"FraudPreventionTeam updated (Claim #{instance.claimid.claimId}): {'; '.join(changes)}"
                logger.info(f"Creating notification: {message}")
                notification = Admin_notification.objects.create(
                    message=message,
                    fraud_team=instance
                )
                broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_delete, sender=FraudPreventionTeam)
def notify_fraud_team_delete(sender, instance, **kwargs):
    """Handle FraudPreventionTeam deletion."""
    message = f"FraudPreventionTeam removed from Claim #{instance.claimid.claimId}: {instance.investigatorName}"
    logger.info(f"Creating notification: {message}")
    notification = Admin_notification.objects.create(message=message)
    broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_save, sender=Officer)
def notify_officer(sender, instance, created, **kwargs):
    """Handle Officer create/update."""
    if created:
        message = f"New Officer assigned to Claim #{instance.claim.claimId}: {instance.officerName}"
        logger.info(f"Creating notification: {message}")
        notification = Admin_notification.objects.create(
            message=message,
            officer=instance
        )
        broadcast_notification(message, notification.created_at.isoformat(), notification.id)
    else:
        previous = previous_instances.pop((sender, instance.pk), None)
        if previous:
            changes = []
            if previous.officerName != instance.officerName:
                changes.append(f"Name changed from '{previous.officerName}' to '{instance.officerName}'")
            if changes:
                message = f"Officer updated (Claim #{instance.claim.claimId}): {'; '.join(changes)}"
                logger.info(f"Creating notification: {message}")
                notification = Admin_notification.objects.create(
                    message=message,
                    officer=instance
                )
                broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_delete, sender=Officer)
def notify_officer_delete(sender, instance, **kwargs):
    """Handle Officer deletion."""
    message = f"Officer removed from Claim #{instance.claim.claimId}: {instance.officerName}"
    logger.info(f"Creating notification: {message}")
    notification = Admin_notification.objects.create(message=message)
    broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_save, sender=Case)
def notify_case(sender, instance, created, **kwargs):
    """Handle Case create/update."""
    if created:
        message = f"New Case created: #{instance.caseID} by Officer {instance.officer.officerName}"
        logger.info(f"Creating notification: {message}")
        notification = Admin_notification.objects.create(
            message=message,
            case=instance
        )
        broadcast_notification(message, notification.created_at.isoformat(), notification.id)
    else:
        previous = previous_instances.pop((sender, instance.pk), None)
        if previous:
            changes = []
            if previous.status != instance.status:
                changes.append(f"Status changed from '{previous.status}' to '{instance.status}'")
            if changes:
                message = f"Case updated (#{instance.caseID}): {'; '.join(changes)}"
                logger.info(f"Creating notification: {message}")
                notification = Admin_notification.objects.create(
                    message=message,
                    case=instance
                )
                broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_delete, sender=Case)
def notify_case_delete(sender, instance, **kwargs):
    """Handle Case deletion."""
    message = f"Case deleted: #{instance.caseID}"
    logger.info(f"Creating notification: {message}")
    notification = Admin_notification.objects.create(message=message)
    broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_save, sender=PendingBeneficiary)
def notify_pending_beneficiary(sender, instance, created, **kwargs):
    """Handle PendingBeneficiary create/update."""
    if created:
        message = f"New Pending Beneficiary added to Policy #{instance.policy.policyId}: {instance.name}"
        logger.info(f"Creating notification: {message}")
        notification = Admin_notification.objects.create(
            message=message,
            policy=instance.policy
        )
        broadcast_notification(message, notification.created_at.isoformat(), notification.id)
    else:
        previous = previous_instances.pop((sender, instance.pk), None)
        if previous:
            changes = []
            if previous.name != instance.name:
                changes.append(f"Name changed from '{previous.name}' to '{instance.name}'")
            if changes:
                message = f"Pending Beneficiary updated (Policy #{instance.policy.policyId}): {'; '.join(changes)}"
                logger.info(f"Creating notification: {message}")
                notification = Admin_notification.objects.create(
                    message=message,
                    policy=instance.policy
                )
                broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_delete, sender=PendingBeneficiary)
def notify_pending_beneficiary_delete(sender, instance, **kwargs):
    """Handle PendingBeneficiary deletion."""
    message = f"Pending Beneficiary removed from Policy #{instance.policy.policyId}: {instance.name}"
    logger.info(f"Creating notification: {message}")
    notification = Admin_notification.objects.create(message=message)
    broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_save, sender=ApprovalRequest)
def notify_approval_request(sender, instance, created, **kwargs):
    """Handle ApprovalRequest create/update."""
    if created:
        message = f"New Approval Request created: Token {instance.token}"
        logger.info(f"Creating notification: {message}")
        notification = Admin_notification.objects.create(
            message=message,
            insured_person=instance.insured_person
        )
        broadcast_notification(message, notification.created_at.isoformat(), notification.id)
    else:
        previous = previous_instances.pop((sender, instance.pk), None)
        if previous:
            changes = []
            if previous.status != instance.status:
                changes.append(f"Status changed from '{previous.status}' to '{instance.status}'")
            if changes:
                message = f"Approval Request updated (Token {instance.token}): {'; '.join(changes)}"
                logger.info(f"Creating notification: {message}")
                notification = Admin_notification.objects.create(
                    message=message,
                    insured_person=instance.insured_person
                )
                broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_delete, sender=ApprovalRequest)
def notify_approval_request_delete(sender, instance, **kwargs):
    """Handle ApprovalRequest deletion."""
    message = f"Approval Request deleted: Token {instance.token}"
    logger.info(f"Creating notification: {message}")
    notification = Admin_notification.objects.create(message=message)
    broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_save, sender=Notification)
def notify_notification(sender, instance, created, **kwargs):
    """Handle Notification create/update."""
    if created:
        message = f"New Notification created for User {instance.user.username}: {instance.message}"
        logger.info(f"Creating notification: {message}")
        notification = Admin_notification.objects.create(
            message=message,
            policy=instance.related_policy
        )
        broadcast_notification(message, notification.created_at.isoformat(), notification.id)
    else:
        previous = previous_instances.pop((sender, instance.pk), None)
        if previous:
            changes = []
            if previous.read != instance.read:
                changes.append(f"Read status changed from {previous.read} to {instance.read}")
            if changes:
                message = f"Notification updated for User {instance.user.username}: {'; '.join(changes)}"
                logger.info(f"Creating notification: {message}")
                notification = Admin_notification.objects.create(
                    message=message,
                    policy=instance.related_policy
                )
                broadcast_notification(message, notification.created_at.isoformat(), notification.id)

@receiver(post_delete, sender=Notification)
def notify_notification_delete(sender, instance, **kwargs):
    """Handle Notification deletion."""
    message = f"Notification deleted for User {instance.user.username}: {instance.message}"
    logger.info(f"Creating notification: {message}")
    notification = Admin_notification.objects.create(message=message)
    broadcast_notification(message, notification.created_at.isoformat(), notification.id)

print("Signals loaded")  # Debug