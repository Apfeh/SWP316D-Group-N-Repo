from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import ApprovalRequest, Notification, PolicyHolder
from datetime import timedelta

class Command(BaseCommand):
    help = 'Checks for expired approval requests and cleans up'
    
    def handle(self, *args, **options):
        # Get expired approval requests
        expired_requests = ApprovalRequest.objects.filter(
            expires_at__lt=timezone.now(),
            status='pending'
        )
        
        for request in expired_requests:
            # Update status to expired
            request.status = 'expired'
            request.save()
            
            # Get policyholder from stored data
            policy_data = json.loads(request.policy_data)
            try:
                policy_holder = PolicyHolder.objects.get(id=policy_data['policy_holder_id'])
                
                # Create notification
                Notification.objects.create(
                    user=policy_holder.user,
                    message="An approval request has expired without confirmation",
                    notification_type='policy_expired'
                )
                
                self.stdout.write(f"Expired approval handled for {policy_holder.user.email}")
            except PolicyHolder.DoesNotExist:
                self.stdout.write("Policyholder not found for expired approval")
        
        self.stdout.write(f"Processed {len(expired_requests)} expired approvals")