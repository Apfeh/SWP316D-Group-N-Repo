from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import Policy
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

REMINDER_DAYS = [30, 7, 1]  # Customize this as needed

def send_policy_renewal_reminders():
    logger.info("🕒 Running policy renewal reminder check...")

    now = timezone.now().date()  # Strip time part for comparison

    for days_before in REMINDER_DAYS:
        target_date = now + timezone.timedelta(days=days_before)
        expiring_policies = Policy.objects.filter(expiration_date__date=target_date, status='active')

        if expiring_policies.exists():
            logger.info(f"🔍 Found {expiring_policies.count()} policies expiring in {days_before} days.")

        for policy in expiring_policies:
            email = policy.policyHolder.email
            name = policy.policyHolder.name
            subject = f"⏰ {days_before}-Day Reminder: Renew Your Policy"

            renewal_link = f"http://127.0.0.1:8000/login"

            message = f"""
Hello {name},

Your insurance policy (ID: {policy.policyId}) is set to expire on {policy.expiration_date.date()}.

➤ Please log into your dashboard and renew your policy before it expires:
{renewal_link}

Stay safe,  
Fraud Shield Insurance 🛡️
"""

            try:
                send_mail(subject, message.strip(), settings.DEFAULT_FROM_EMAIL, [email])
                logger.info(f"📨 Reminder sent to {email} for policy {policy.policyId}")
            except Exception as e:
                logger.error(f"❌ Failed to send reminder to {email}: {e}")

def check_expired_policies():
    now = timezone.now()
    expired_policies = Policy.objects.filter(expiration_date__lte=now, status='active')

    if expired_policies.exists():
        logger.info(f"💀 Marking {expired_policies.count()} policies as expired...")

    for policy in expired_policies:
        policy.status = 'expired'
        policy.save()

        try:
            send_mail(
                "🚫 Policy Expired",
                f"""
Hey {policy.policyHolder.name},

Your insurance policy (ID: {policy.policyId}) expired on {policy.expiration_date.date()}.

Please contact our support team if you believe this is an error or need further assistance.

Fraud Shield Insurance 🛡️
""".strip(),
                settings.DEFAULT_FROM_EMAIL,
                [policy.policyHolder.email]
            )
            logger.info(f"⚰️ Expiration notice sent for policy {policy.policyId}")
        except Exception as e:
            logger.error(f"Failed to send expiration email for policy {policy.policyId}: {e}")

# Scheduler config
scheduler = BackgroundScheduler()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(send_policy_renewal_reminders, 'interval', hours=24, id='reminder_job', replace_existing=True)
        scheduler.add_job(check_expired_policies, 'interval', hours=1, id='expiration_job', replace_existing=True)
        scheduler.start()
        logger.info("💡 APScheduler started for policy reminders and expiration checks.")
    else:
        logger.info("⚙️ Scheduler already running.")
