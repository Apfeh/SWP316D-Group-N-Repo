from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from IFPWebApp.models import Policy, Claim, PolicyHolder, Beneficiary, InsuredPerson, FraudPreventionTeam, Officer, Case, Admin_notification

@receiver(post_save, sender=InsuredPerson)
def notify_new_insured_person(sender, instance, created, **kwargs):
    if created:
        try:
            print(f"Signal triggered for InsuredPerson: {instance.name}")  # Debug
            policy_id = instance.policy_id.policyId if instance.policy_id else "Unknown"
            message = f"New insured person {instance.name} added to Policy #{policy_id}."
            notification = Admin_notification.objects.create(
                message=message,
                insured_person=instance
            )
            print(f"InsuredPerson notification created: {message} (ID: {notification.id})")  # Debug
            broadcast_notification(message, notification.created_at.isoformat(), notification.id)
        except Exception as e:
            print(f"Error in notify_new_insured_person: {e}")

def broadcast_notification(message, created_at, notification_id):
    try:
        print(f"Broadcasting notification: {message} (ID: {notification_id})")  # Debug
        channel_layer = get_channel_layer()
        if channel_layer is None:
            print("Error: Channel layer is not configured")
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
        print(f"Error in broadcast_notification: {e}")