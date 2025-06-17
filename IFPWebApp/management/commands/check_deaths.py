# insurance/management/commands/notify_beneficiaries.py
from django.core.management.base import BaseCommand
from IFPWebApp.models import DeathCertificate
from IFPWebApp.models import InsuredPerson, Beneficiary
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Checks if insured persons are deceased and notifies beneficiaries'

    def handle(self, *args, **kwargs):
        deceased_ids = set(DeathCertificate.objects.values_list('idNumber__idNumber', flat=True))
        insured_persons = InsuredPerson.objects.all()

        for person in insured_persons:
            if person.id_number in deceased_ids:
                # Update status to deceased (optional)
                if person.status != 'deceased':
                    person.status = 'deceased'
                    person.save()

                # Find the beneficiary
                try:
                    beneficiary = Beneficiary.objects.get(policy=person.policy_id)
                except Beneficiary.DoesNotExist:
                    self.stdout.write(f"No beneficiary found for policy {person.policy_id.policyId}")
                    continue

                # Send email
                send_mail(
                    subject='Notice: Insured Person Has Been Declared Deceased',
                    message=(
                        f"Dear {beneficiary.name},\n\n"
                        f"We regret to inform you that {person.name}, the insured individual under policy number {person.policy_id.policyId}, "
                        "has been officially marked as deceased in the National Citizen Register.\n\n"
                        "As the designated beneficiary, you may now initiate the claims process.\n\n"
                        "Please log in to your account using the link below to begin:\n"
                        "http://127.0.0.1:8000/beneficiary/login/\n\n"
                        "If you have any questions or need assistance, feel free to contact our support team.\n\n"
                        "Sincerely,\n"
                        "The Insurance Claims Department"
                    ),
                    from_email='noreply@insurance-system.com',
                    recipient_list=[beneficiary.email],
                    fail_silently=False,
                )

                self.stdout.write(f"Email sent to beneficiary of {person.name}")
            else:
                self.stdout.write(f"{person.name} is still alive.")