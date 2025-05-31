# email_utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_django_email(subject, to_email, template_name, context):
    """Send an email using Django's built-in email functionality"""
    try:
        # Ensure we have proper email settings
        if not hasattr(settings, 'EMAIL_HOST_USER') or not settings.EMAIL_HOST_USER:
            logger.error("Email settings not configured properly")
            return False
            
        html_content = render_to_string(template_name, context)
        plain_content = strip_tags(html_content)
        
        send_mail(
            subject=subject,
            message=plain_content,
            html_message=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}", exc_info=True)
        return False

def send_otp_email(otp_code, recipient):
    """Send OTP email with proper template path"""
    context = {
        'otp_code': otp_code, 
        'valid_minutes': 3,
        'support_email': getattr(settings, 'SUPPORT_EMAIL', 'support@example.com')
    }
    
    # Use the correct template path
    template_path = 'emails/otp_email.html'  # Ensure this path is correct
    
    return send_django_email(
        subject='Your OTP Verification Code',
        to_email=recipient,
        template_name=template_path,
        context=context
    )