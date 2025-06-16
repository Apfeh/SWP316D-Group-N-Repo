# your_app/notifications.py

from django.core.mail import send_mail
from django.conf import settings
from IFPWebApp.models import PolicyHolder


from django.core.mail import send_mail
from django.conf import settings
from IFPWebApp.models import PolicyHolder

def send_claim_status_email(recipient_email, claim_status):
    try:
        policyholder = PolicyHolder.objects.get(email=recipient_email)
        policyholder_name = policyholder.name
    except PolicyHolder.DoesNotExist:
        policyholder_name = "Policyholder"

    subject = "Claim Status Update"
    message = (
        f"Dear {policyholder_name},\n\n"
        f"Your claim status has been updated to: {claim_status}.\n\n"
        "Thank you."
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],
        fail_silently=False,
    )



 