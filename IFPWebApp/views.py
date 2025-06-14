from django.shortcuts import render, redirect, get_object_or_404
from .models import Beneficiary

from .models import Claim

from .models import InsuredPerson
from django.urls import reverse
from .models import PolicyHolder
from django.http import HttpResponseNotAllowed
from django.http import HttpResponse
from django.contrib import messages
from .models import Policy
from django.contrib.auth.hashers import make_password

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import PolicyHolder
from .fraud_detection import run_automatic_checks






def landing_page(request):
    return render(request, 'landing_page.html')

def login(request):
    return render(request, 'registration/login.html')

def register(request):
    return render(request, 'register.html')

def contact(request):
    return render(request, 'contact.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')
from django.contrib.auth.decorators import login_required
@login_required
def logout(request):
    return render(request, 'landing_page.html')

def beneficiary_list(request):
    beneficiaries = Beneficiary.objects.all()
    return render(request, 'beneficiary_list.html', {'beneficiaries': beneficiaries})



#InsuredPerson view
def index(request):
    insured_persons = InsuredPerson.objects.all()
    return render(request, 'insured_persons.html', {'insured_persons': insured_persons})

def delete_insured_person(request, id):
    person = get_object_or_404(InsuredPerson, id=id)
    if request.method == 'POST':
        person.delete()
        return redirect(reverse('insured_persons_list'))
    return redirect(reverse('insured_persons_list'))

#Policy Holder
def dashboard(request):
    return render(request, 'Policyholder Pages/dashboard.html')

# List all PolicyHolders
def list_policyholders(request):
    policyholders = PolicyHolder.objects.all()
    return render(request, 'list.html', {'policyholders': policyholders})

# Add new PolicyHolder
def add_policyholder(request):
    if request.method == "POST":
        policyHolderId = request.POST.get('policyHolderId')
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        password = request.POST.get('password')

        PolicyHolder.objects.create(
            policyHolderId=policyHolderId,
            name=name,
            address=address,
            contact=contact,
            email=email,
            password=make_password(password)
        )
        return redirect('dashboard')
    return render(request, 'add.html')

# Update a PolicyHolder


# List all PolicyHolders
def list_policyholders(request):
    policyholders = PolicyHolder.objects.all()
    return render(request, 'list.html', {'policyholders': policyholders})

# Add new PolicyHolder
def add_policyholder(request):
    if request.method == "POST":
        id_number = request.POST.get('id_number')
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        password = request.POST.get('password')  # Consider hashing in real usage

        PolicyHolder.objects.create(
            id_number=id_number,
            name=name,
            address=address,
            contact=contact,
            email=email,
            password=password
        )
        return redirect('dashboard')

    return render(request, 'add.html')

# Update a PolicyHolder
def update_policyholder(request, id):
    try:
        policyholder = PolicyHolder.objects.get(policyHolderId=id)
    except PolicyHolder.DoesNotExist:
        return HttpResponse("PolicyHolder not found", status=404)

    if request.method == "POST":
        policyholder.name = request.POST.get('name')
        policyholder.address = request.POST.get('address')
        policyholder.contact = request.POST.get('contact')
        policyholder.email = request.POST.get('email')
        policyholder.save()
        return redirect('list_policyholders')
    
    return render(request, 'update.html', {'policyholder': policyholder})




# Dalphy's Beneficiary Pages
def add_beneficiary(request):
    return render(request, "add_beneficiary.html")



def beneficiary_dashboard(request):
    beneficiary_id = request.session.get('beneficiary_id')

    if not beneficiary_id:
        return redirect('login')  # or 'beneficiary_login' if that's your login route

    beneficiary = Beneficiary.objects.filter(beneficiaryId=beneficiary_id).first()

    latest_claim = None
    if beneficiary:
        latest_claim = Claim.objects.filter(beneficiaryId=beneficiary).order_by('-dateFiled').first()

    if latest_claim:
        claim_summary = {
            'beneficiary_name': beneficiary.name,
            'current_status': latest_claim.status,
            'claim_amount': getattr(latest_claim, 'claimAmount', 0),
            'previous_claims': Claim.objects.filter(beneficiaryId=beneficiary).exclude(claimId=latest_claim.claimId).count()
        }
    else:
        claim_summary = {
            'beneficiary_name': beneficiary.name if beneficiary else "Unknown",
            'current_status': 'No claims',
            'claim_amount': 0,
            'previous_claims': 0
        }

    return render(request, 'Beneficiary/beneficiary_dashboard.html', {'claim_summary': claim_summary})


def beneficiary_list(request):
    return render(request, "beneficiary_list.html")

def beneficiary_verification(request):
    return render(request, "beneficiary_verification.html")

def claim_status(request):
    return render(request, "claim_status.html")

def edit_beneficiary(request):
    return render(request, "edit_beneficiary.html")

def file_claim(request):
    return render(request, "file_claim.html")

# Insured Person Pages
def add_insured_person(request):
    return render(request, "add_insured_person.html")

def consent_verification(request):
    return render(request, "consent_verification.html")

def insured_dashboard(request):
    return render(request, "dashboard.html")  # reused dashboard
    # if you prefer a different template, you can change here

def policy_details(request):
    return render(request, "policy_details.html")

# Nyiko's Law Enforcement Pages
def law_dashboard(request):
    return render(request, "dashboard.html")  # reused dashboard
    # if law has their own dashboard.html, differentiate later

def fraud_case_details(request):
    return render(request, "fraud_case_details.html")

def fraud_database_search(request):
    return render(request, "fraud_database_search.html")

def law_login(request):
    return render(request, "login.html")


# Landing and Authentication

def landing_page(request):
     request.session.flush()
     return render(request, 'landing_page.html')

def login(request):
    return render(request, 'registration/login.html')


# Insured Person Views

def index(request):
    insured_persons = InsuredPerson.objects.all()
    return render(request, 'insured_persons.html', {'insured_persons': insured_persons})

def delete_insured_person(request, id):
    person = get_object_or_404(InsuredPerson, id=id)
    if request.method == 'POST':
        person.delete()
        return redirect(reverse('insured_persons_list'))
    return redirect(reverse('insured_persons_list'))

# PolicyHolder Views


def list_policyholders(request):
    policyholders = PolicyHolder.objects.all()
    return render(request, 'list.html', {'policyholders': policyholders})

def add_policyholder(request):
    if request.method == "POST":
        policyHolderId = request.POST.get('policyHolderId')
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        PolicyHolder.objects.create(
            policyHolderId=policyHolderId,
            name=name,
            address=address,
            contact=contact,
            email=email
        )
        return redirect('dashboard')
    return render(request, 'add.html')

def update_policyholder(request, id):
    try:
        policyholder = PolicyHolder.objects.get(policyHolderId=id)
    except PolicyHolder.DoesNotExist:
        return HttpResponse("PolicyHolder not found", status=404)

    if request.method == "POST":
        policyholder.name = request.POST.get('name')
        policyholder.address = request.POST.get('address')
        policyholder.contact = request.POST.get('contact')
        policyholder.email = request.POST.get('email')
        policyholder.save()
        return redirect('list_policyholders')

    return render(request, 'update.html', {'policyholder': policyholder})



# Static/Dashboard Views

def add_beneficiary(request):
    return render(request, "add_beneficiary.html")

def beneficiary_verification(request):
    return render(request, "beneficiary_verification.html")

def claim_status(request):
    return render(request, "claim_status.html")

def edit_beneficiary(request):
    return render(request, "edit_beneficiary.html")

def file_claim(request):
    return render(request, "file_claim.html")

def add_insured_person(request):
    return render(request, "add_insured_person.html")

def consent_verification(request):
    return render(request, "consent_verification.html")

def insured_dashboard(request):
    return render(request, "dashboard.html")

def policy_details(request):
    return render(request, "policy_details.html")

def law_dashboard(request):
    return render(request, "dashboard.html")

def fraud_case_details(request):
    return render(request, "fraud_case_details.html")

def fraud_database_search(request):
    return render(request, "fraud_database_search.html")

def law_login(request):
    return render(request, "login.html")


def home(request):
    return render(request, 'boitshepo/home.html')

POLICIES = [
    {'id': 1, 'holder_name': 'John Doe', 'insured_persons': 'Jane Doe', 'risk_score': 75, 'status': 'Pending'},
    {'id': 2, 'holder_name': 'Alice Smith', 'insured_persons': 'Bob Smith', 'risk_score': 55, 'status': 'Pending'},
    {'id': 3, 'holder_name': 'Mark Johnson', 'insured_persons': 'Lucy Johnson', 'risk_score': 85, 'status': 'Pending'},
]

# IFPWebApp/views_fraud.py


def run_manual_fraud_check(request, policyholder_id):
    policyholder = get_object_or_404(PolicyHolder, id=policyholder_id)
    run_automatic_checks(policyholder)
    messages.success(request, f"Fraud check run for {policyholder.name}")
    return redirect('policyholder_detail', policyholder_id=policyholder.id)  # adjust to your actual view


#======================================================================================================================================
# IFPWebApp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Policy, PolicyHolder, InsuredPerson, Beneficiary, Claim
from django.core.files.storage import FileSystemStorage
from .forms import CustomRegistrationForm
import logging

# Set up logging
logger = logging.getLogger(__name__)

def register(request):
  
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '')
            return redirect('send_otp')
        else:
            logger.debug(f"Form errors: {form.errors}")
            messages.error(request, 'Registration failed. Please check the form.')
    else:
        form = CustomRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def log_register(request):
    messages.warning(request, 'You are already logged in. Redirected to dashboard.')
    return redirect('dashboard')

@login_required
def dashboard(request):
    logger.debug(f"User email: {request.user.email}")
    try:
        # Change from email= to user__email=
        policy_holder = PolicyHolder.objects.get(user__email=request.user.email)
        logger.debug(f"Found PolicyHolder: {policy_holder.id_number}")
        #active_policies = Policy.objects.filter(policy_holder=policy_holder).count()
        active_policies = Policy.objects.filter(policyHolder=policy_holder).count()
        pending_claims = Claim.objects.filter(policyId__policyHolder=policy_holder, status='Pending').count()


        
        notifications = pending_claims
        name = policy_holder.name  # Ensure this field exists in PolicyHolder
        
    except PolicyHolder.DoesNotExist:
        logger.warning(f"No PolicyHolder found for email: {request.user.email}")
        active_policies = 0
        pending_claims = 0
        notifications = 0
        name = "User"
        messages.error(request, 'No policyholder profile found. Please contact support.')
    
    context = {
        'active_policies': active_policies,
        'pending_claims': pending_claims,
        'notifications': notifications,
        'name': name,
    }
    return render(request, 'Policyholder Pages/dashboard.html', context)




from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Citizen, Policy, InsuredPerson, PolicyHolder, ApprovalRequest
import uuid
from datetime import date, timedelta
import logging

logger = logging.getLogger(__name__)
@login_required
def get_citizen(request):
    id_number = request.GET.get('id_number')
    try:
        citizen = Citizen.objects.get(idNumber=id_number)
        return JsonResponse({
            'name': citizen.name,
            'surname': citizen.surname,
            'dateOfBirth': citizen.dateOfBirth.strftime('%Y-%m-%d'),
        })
    except Citizen.DoesNotExist:
        return JsonResponse({'error': 'Citizen not found in national database'}, status=404)


from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.conf import settings
from .models import PolicyHolder, Citizen, Policy, InsuredPerson, ApprovalRequest, Notification, Claim
import uuid
import logging
from datetime import timedelta
import json

logger = logging.getLogger(__name__)

@login_required
def add_policy(request):
    logger.debug(f"User email: {request.user.email}")
    try:
        policy_holder = PolicyHolder.objects.get(user__email=request.user.email)
        logger.debug(f"Found PolicyHolder: {policy_holder.user.email}")
    except PolicyHolder.DoesNotExist:
        logger.warning(f"No PolicyHolder found for email: {request.user.email}")
        messages.error(request, 'No policyholder profile found. Please contact support.')
        return redirect('dashboard')

    if request.method == 'POST':
        insured_id = request.POST.get('insured_id')
        is_underage = request.POST.get('is_underage') == 'on'
        parent_id = request.POST.get('parent_id') if is_underage else None
        contact_email = request.POST.get('contact_email')
        contact_phone = request.POST.get('contact_phone')
        relationship = request.POST.get('relationship')
        policy_type = request.POST.get('policy_type')
        confirmed_status = request.POST.get('confirmed_status')
        parent_confirmed_status = request.POST.get('parent_confirmed_status')
        relationship_docs = request.FILES.get('relationship_docs')
        
        # Validate confirmations
        if confirmed_status != '1':
            messages.error(request, 'Please confirm insured person details')
            return redirect('add_policy')
            
        if is_underage and parent_confirmed_status != '1':
            messages.error(request, 'Please confirm parent details')
            return redirect('add_policy')
        
        try:
            insured_citizen = Citizen.objects.get(idNumber=insured_id)
        except Citizen.DoesNotExist:
            messages.error(request, 'Insured person not found in national database')
            return redirect('add_policy')
        
        # Store document if provided
        doc_path = None
        if relationship_docs:
            fs = FileSystemStorage()
            filename = fs.save(relationship_docs.name, relationship_docs)
            doc_path = fs.url(filename)
        
        # Prepare policy data for approval request
        policy_data = {
            'policy_holder_id': policy_holder.id_number,
            'policy_type': policy_type,
            'insured_name': f"{insured_citizen.name} {insured_citizen.surname}",
            'insured_dob': insured_citizen.dateOfBirth.isoformat(),
            'relationship': relationship,
            'id_number': insured_id,
            'parent_id_number': parent_id,
            'contact_email': contact_email,
            'contact_phone': contact_phone,
            'document_path': doc_path,
            'is_underage': is_underage,
        }
        
        # Create approval request (policy not created yet)
        expires_at = timezone.now() + timedelta(days=7)
        approval_request = ApprovalRequest(
            policy_data=json.dumps(policy_data),
            expires_at=expires_at
        )
        approval_request.save()
        
        # Send approval email
        approval_url = request.build_absolute_uri(
            f'/approve-insured/{approval_request.token}/'
        )
        
        if is_underage:
            try:
                parent_citizen = Citizen.objects.get(idNumber=parent_id)
                recipient_name = f"{parent_citizen.name} {parent_citizen.surname}"
            except Citizen.DoesNotExist:
                recipient_name = "Parent/Guardian"
        else:
            recipient_name = f"{insured_citizen.name} {insured_citizen.surname}"
        
        subject = "Action Required: Approval for Insurance Coverage"
        message = f"""
        Dear {recipient_name},
        
        {policy_holder.name} has added you as an insured person for a new policy.
        
        Insured Person Details:
        - Name: {insured_citizen.name} {insured_citizen.surname}
        - ID Number: {insured_id}
        - Date of Birth: {insured_citizen.dateOfBirth}
        - Relationship: {relationship}
        
        To approve this coverage, please click the link below and enter your ID number:
        {approval_url}
        
        This link expires in 7 days.
        
        If you did not authorize this, please ignore this email or contact our support team.
        
        Regards,
        FraudShield Team
        """
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [contact_email],
            fail_silently=False,
        )
        
        # Create notification for policyholder
        Notification.objects.create(
            user=request.user,
            message=f"Approval request sent to {recipient_name} for policy creation",
            notification_type='approval_sent',
            related_policy=None
        )
        
        approval_request.notification_sent = True
        approval_request.save()
        
        messages.success(request, 'Approval request sent to insured person. Policy will be created after approval.')
        return redirect('dashboard')

    return render(request, 'Policyholder Pages/add-policy.html')

def approve_insured_person(request, token):
    try:
        approval_request = ApprovalRequest.objects.get(token=token)
        
        # Check if approval request has expired
        if timezone.now() > approval_request.expires_at:
            approval_request.status = 'expired'
            approval_request.save()
            return render(request, 'approval_error.html', {
                'message': 'This approval link has expired'
            })
            
    except ApprovalRequest.DoesNotExist:
        return render(request, 'approval_error.html', {
            'message': 'Invalid approval link'
        })
    
    if request.method == 'POST':
        entered_id = request.POST.get('id_number')
        policy_data = json.loads(approval_request.policy_data)
        
        # Check if entered ID matches insured person or parent
        if (entered_id == policy_data['id_number'] or 
            (policy_data['is_underage'] and entered_id == policy_data['parent_id_number'])):
            
            # Create the actual policy now that it's approved
            policy_holder = PolicyHolder.objects.get(id_number=policy_data['policy_holder_id'])
            
            policy = Policy(
                policyHolder=policy_holder,
                policyType=policy_data['policy_type'],
                premiumAmount=0.00,
                startDate=timezone.now().date(),
                endDate=timezone.now().date() + timedelta(days=365),
                status='active',
                expiration_date=timezone.now() + timedelta(days=7)
            )
            policy.save()
            
            # Create insured person
            insured_person = InsuredPerson(
                policy_id=policy,
                name=policy_data['insured_name'],
                date_of_birth=policy_data['insured_dob'],
                relationship_to_policy_holder=policy_data['relationship'],
                holder=policy_holder,
                id_number=policy_data['id_number'],
                parent_id_number=policy_data['parent_id_number'],
                contact_email=policy_data['contact_email'],
                contact_phone=policy_data['contact_phone']
            )
            insured_person.save()
            
            # Update approval request
            approval_request.insured_person = insured_person
            approval_request.status = 'approved'
            approval_request.save()
            
            # Create notification for policyholder
            Notification.objects.create(
                user=policy_holder.user,
                message=f"Policy #{policy.policyId} has been approved by {insured_person.name}",
                notification_type='approval_received',
                related_policy=policy
            )
            
            return render(request, 'approval_success.html')
        else:
            return render(request, 'approval_page.html', {
                'error': 'ID number does not match',
                'token': token
            })
    
    return render(request, 'approval_page.html', {'token': token})
@login_required
def notifications(request):
    # Get pending claims
    try:
        policy_holder = PolicyHolder.objects.get(email=request.user.email)
        pending_claims = Claim.objects.filter(
            policyId__policyHolder=policy_holder,
            status='Pending'
        )
    except PolicyHolder.DoesNotExist:
        pending_claims = []
    
    # Get user notifications
    # First: Mark all unread notifications as read
    unread_notifications = Notification.objects.filter(
        user=request.user,
        read=False
    )
    unread_notifications.update(read=True)
    
    # Then: Get the last 10 notifications for display
    user_notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]
    
    context = {
        'pending_claims': pending_claims,
        'notifications': user_notifications
    }
    return render(request, 'Policyholder Pages/notifications.html', context)
@login_required
def policy_status(request):
    logger.debug(f"User email: {request.user.email}")
    try:
        policy_holder = PolicyHolder.objects.get(email=request.user.email)
        policies = Policy.objects.filter(policyHolder=policy_holder)
    except PolicyHolder.DoesNotExist:
        messages.error(request, 'No policyholder profile found.')
        return redirect('dashboard')
    
    # Calculate days remaining for pending policies
    for policy in policies:
        if policy.status == 'pending':
            policy.days_remaining = (policy.expiration_date - timezone.now()).days
    
    context = {'policies': policies}
    return render(request, 'Policyholder Pages/policy-status.html', context)

from django.core.mail import send_mail
from django.urls import reverse
from uuid import uuid4
from .models import PendingBeneficiary

@login_required
def manage_beneficiaries(request):
    try:
        policy_holder = PolicyHolder.objects.get(user__email=request.user.email)
    except PolicyHolder.DoesNotExist:
        messages.error(request, 'No policyholder profile found.')
        return redirect('dashboard')

    if request.method == 'POST':
        policy_id = request.POST.get('policy_id')
        beneficiary_name = request.POST.get('beneficiary_name')
        beneficiary_email = request.POST.get('beneficiary_contact')
        relationship = request.POST.get('relationship')

        try:
            policy = Policy.objects.get(policyId=policy_id, policyHolder=policy_holder)
            token = uuid4().hex
            
            # Create pending beneficiary
            PendingBeneficiary.objects.create(
                policy=policy,
                name=beneficiary_name,
                email=beneficiary_email,
                relationship=relationship,
                token=token
            )
            
            # Send approval email
            approval_url = request.build_absolute_uri(
                reverse('approve_beneficiary', kwargs={'token': token})
            )
            decline_url = request.build_absolute_uri(
                reverse('decline_beneficiary', kwargs={'token': token})
            )
            
            send_mail(
                
    subject='Action Required: Beneficiary Approval Request',
    message=f'Please approve or decline being added as a beneficiary:\n\n'
            f'Approve: {approval_url}\nDecline: {decline_url}',
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=[beneficiary_email],
    html_message=f'''
        <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f9f9f9; color: #333;">
            <div style="max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h2 style="color: #2F2B43;">Beneficiary Approval Request</h2>
                <p>Dear Beneficiary,</p>
                <p>You have been nominated to be added as a beneficiary. Please confirm your choice by clicking one of the buttons below:</p>

                <div style="margin: 20px 0;">
                    <a href="{approval_url}" style="display: inline-block; background-color: #4CAF50; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin-right: 10px;">
                        Approve
                    </a>
                    <a href="{decline_url}" style="display: inline-block; background-color: #f44336; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">
                        Decline
                    </a>
                </div>

                <p>If you were not expecting this email, you may ignore it.</p>
                <p style="font-size: 12px; color: #777;">This message was sent automatically. Please do not reply.</p>
            </div>
        </div>
    ''',
    fail_silently=False

            )
            
            messages.success(request, 'Approval request sent to beneficiary.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        
        return redirect('manage_beneficiaries')

    # GET request handling remains similar
    pending = PendingBeneficiary.objects.filter(policy__policyHolder=policy_holder)
    beneficiaries = Beneficiary.objects.filter(policy__policyHolder=policy_holder)
    
    return render(request, 'Policyholder Pages\manage-beneficiaries.html', {
        'policy_options': Policy.objects.filter(policyHolder=policy_holder),
        'beneficiaries': beneficiaries,
        'pending_beneficiaries': pending
    })

def approve_beneficiary(request, token):
    try:
        pending = PendingBeneficiary.objects.get(token=token)
        # Create actual beneficiary
        Beneficiary.objects.create(
            policy=pending.policy,
            name=pending.name,
            contactNumber=pending.email,
            relationshipToInsured=pending.relationship
        )
        pending.delete()
        return render(request, 'approval_response.html', {'approved': True})
    except PendingBeneficiary.DoesNotExist:
        return render(request, 'approval_response.html', {'invalid': True})

def decline_beneficiary(request, token):
    try:
        pending = PendingBeneficiary.objects.get(token=token)
        pending.delete()
        return render(request, 'approval_response.html', {'approved': False})
    except PendingBeneficiary.DoesNotExist:
        return render(request, 'approval_response.html', {'invalid': True})

@login_required
def file_claim(request):
    logger.debug(f"User email: {request.user.email}")
    try:
        policy_holder = PolicyHolder.objects.get(email=request.user.email)
        logger.debug(f"Found PolicyHolder: {policy_holder.user.email}")
    except PolicyHolder.DoesNotExist:
        logger.warning(f"No PolicyHolder found for email: {request.user.email}")
        messages.error(request, 'No policyholder profile found. Please contact support.')
        return redirect('dashboard')

    if request.method == 'POST':
        policy_id = request.POST.get('policy_id')
        death_certificate = request.FILES.get('death_certificate')
        cause_of_death = request.POST.get('cause_of_death')

        try:
            policy = Policy.objects.get(policyId=policy_id, policyHolder=policy_holder)
            beneficiary = Beneficiary.objects.filter(policy=policy).first()
            if not beneficiary:
                messages.error(request, 'No beneficiary found for this policy.')
                return redirect('file_claim')

            claim = Claim(
                policyId=policy,  # or whatever your field is named
                beneficiaryId=beneficiary,
                policyHolderId = policy_holder,
                
                claimAmount=0.00,
                status='Pending'
            )
            claim.save()

            if death_certificate:
                fs = FileSystemStorage()
                filename = fs.save(death_certificate.name, death_certificate)

            messages.success(request, 'Claim filed successfully!')
            return redirect('claim_status')
        except Policy.DoesNotExist:
            messages.error(request, 'Selected policy not found.')
            return redirect('file_claim')

    policy_options = Policy.objects.filter(policyHolder=policy_holder)
    logger.debug(f"Found {policy_options.count()} policy options for PolicyHolder: {policy_holder.user.email}")
    context = {
        'policy_options': policy_options,
    }
    return render(request, 'Policyholder Pages/file-claim.html', context)

@login_required
def claim_status(request):
    logger.debug(f"User email: {request.user.email}")
    try:
        policy_holder = PolicyHolder.objects.get(email=request.user.email)
        logger.debug(f"Found PolicyHolder: {policy_holder.user.email}")
        claims = Claim.objects.filter(policyHolderId=policy_holder)

        logger.debug(f"Found {claims.count()} claims for PolicyHolder: {policy_holder.user.email}")
    except PolicyHolder.DoesNotExist:
        logger.warning(f"No PolicyHolder found for email: {request.user.email}")
        messages.error(request, 'No policyholder profile found. Please contact support.')
        return redirect('dashboard')
    context = {
        'claims': claims,
    }
    return render(request, 'Policyholder Pages/claim-status.html', context)

import base64
import io
import logging
import time
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from .models import Citizen, Photo
import pytesseract
import cv2
import numpy as np
from pdf2image import convert_from_bytes
from datetime import date, datetime, timedelta
from PIL import Image, ImageEnhance


logger = logging.getLogger(__name__)

# ==========================
# BENEFICIARY VERIFICATION
# ==========================


# verification/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import OTP
from django.contrib import messages


import random
from datetime import datetime, timedelta


def send_otp(request):
    if request.method == 'POST':
        email = request.user.email  # Fixed recipient email
        
        # Clear existing OTPs
        OTP.objects.filter(email=email).delete()
        
        # Generate 6-digit OTP
        otp_code = str(random.randint(100000, 999999))
        
        # Set expiration time (3 minutes from now)
        expires_at = timezone.now() + timedelta(minutes=3)
        
        # Create new OTP
        otp = OTP.objects.create(
            email=email,
            otp=otp_code,
            expires_at=expires_at
        )
        
        # Send email
        subject = 'Your Verification OTP'
        message = f'Your OTP is {otp.otp}. It expires in 3 minutes.'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(request, 'OTP sent successfully!')
        return redirect('verify_otp')
    
    return render(request, 'verification/send_otp.html')
from datetime import timedelta

import random

def send_otp(request):
    if request.method == 'POST':
        email = request.user.email   # Or get from request.POST
        
        # Clear existing OTPs for this email
        OTP.objects.filter(email=email).delete()
        
        # Generate 6-digit OTP
        otp_code = str(random.randint(100000, 999999))
        
        # Create new OTP with expiration (3 minutes from now)
        otp = OTP.objects.create(
            email=email,
            otp=otp_code,
            expires_at=timezone.now() + timedelta(minutes=3),
            attempts=0,
            is_verified=False
        )
        
        # Send email
        subject = 'Your Verification OTP'
        message = f'Your OTP is {otp.otp}. It expires in 3 minutes.'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(request, 'OTP sent successfully!')
        return redirect('verify_otp')
    
    return render(request, 'verification/send_otp.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        email = request.user.email  # Or get from session/request
        
        try:
            otp = OTP.objects.get(email=email, is_verified=False)
            
            # Check if OTP is expired using the model method
            if otp.is_expired():
                messages.error(request, 'OTP has expired. Please request a new one.')
                return redirect('send_otp')
            
            if entered_otp == otp.otp:
                otp.is_verified = True
                otp.save()
                return redirect('beneficiary_verification')
            
            messages.error(request, 'Invalid OTP. Please try again.')
            
        except OTP.DoesNotExist:
            messages.error(request, 'OTP not found. Please request a new one.')
            return redirect('send_otp')
    #original is return render(request, 'verification/verify_otp.html')
    return render(request, 'Policyholder Pages\dashboard.html')

def resend_otp(request):
    email = request.user.email  # Or get from session/request
    try:
        otp = OTP.objects.get(email=email)
        if otp.attempts >= 3:
            messages.error(request, 'Maximum resend attempts reached.')
            return redirect('send_otp')
        
        otp.attempts += 1
        otp.save()
        
        # Optionally generate new OTP and update expiration
        otp.otp = str(random.randint(100000, 999999))
        otp.expires_at = timezone.now() + timedelta(minutes=3)
        otp.save()
        
        # Resend email
        subject = 'Your New Verification OTP'
        message = f'Your new OTP is {otp.otp}. It expires in 3 minutes.'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        
        messages.success(request, 'New OTP sent successfully!')
        return redirect('verify_otp')
    
    except OTP.DoesNotExist:
        return redirect('send_otp')
    


#verification for login
# verification/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import OTP
from django.contrib import messages


@login_required
def send_otp1(request):
    if request.method == 'POST':
        email = request.user.email
        # Clear existing OTPS
        OTP.objects.filter(email=email).delete()
        
        # Create new OTP
        otp = OTP.objects.create(email=email)
        
        # Send email
        subject = 'Your Verification OTP'
        message = f'Your OTP is {otp.otp}. It expires in 3 minutes.'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(request, 'OTP sent successfully!')
        return redirect('verify_otp')
    
    return render(request, 'verification/send_otp.html')

def verify_otp1(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        email = 'kutylaalfredo62@gmail.com'
        
        try:
            otp = OTP.objects.get(email=email, is_verified=False)
            if otp.is_expired():
                messages.error(request, 'OTP has expired. Please request a new one.')
                return redirect('send_otp')
            
            if entered_otp == otp.otp:
                otp.is_verified = True
                otp.save()
                return redirect('dashboard')
            
            messages.error(request, 'Invalid OTP. Please try again.')
            
        except OTP.DoesNotExist:
            messages.error(request, 'OTP not found. Please request a new one.')
            return redirect('send_otp')
    
    return render(request, 'verification/verify_otp.html')

def resend_otp1(request):
    email = 'kutylaalfredo62@gmail.com'
    try:
        otp = OTP.objects.get(email=email)
        if otp.attempts >= 3:
            messages.error(request, 'Maximum resend attempts reached.')
            return redirect('send_otp')
        
        otp.attempts += 1
        otp.save()
        return redirect('send_otp')
    
    except OTP.DoesNotExist:
        return redirect('send_otp')

@login_required
def delete_beneficiary(request, beneficiary_id):
    try:
        beneficiary = Beneficiary.objects.get(
            id=beneficiary_id,
            policy__policyHolder__email=request.user.email
        )
        beneficiary.delete()
        messages.success(request, 'Beneficiary removed successfully')
    except Beneficiary.DoesNotExist:
        messages.error(request, 'Beneficiary not found')
    return redirect('manage_beneficiaries')


# views.py

# FACE RECOGNITION (BYPASSED)
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Citizen, Photo
import tempfile
import os
import logging
import io
from django.db import transaction
from IFPWebApp.models import Citizen, Address
from .models import PolicyHolder
from datetime import datetime
import logging
import time
import random
# views.py
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse
from IFPWebApp.models import Citizen
from .models import PolicyHolder
import time
import random
import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Policy, Claim, Admin_notification,ActivityLog  # Replace with actual model names
from django.db.models import Avg

logger = logging.getLogger(__name__)

from django.shortcuts import render
from .ai_engine import assess_policy_risk
from .models import PolicyHolder, Admin


logger = logging.getLogger(__name__)

def risk_reports(request):
    reports = []
    policyholders = PolicyHolder.objects.all()
    logger.info(f"PolicyHolders Count: {policyholders.count()}")

    high = medium = low = 0

    for holder in policyholders:
        risk_data = assess_policy_risk(holder)
        holder.risk_score = risk_data["score"]
        holder.save(update_fields=['risk_score'])

        if risk_data["level"] == "High":
            high += 1
        elif risk_data["level"] == "Medium":
            medium += 1
        else:
            low += 1

        reports.append({
            "id_number": holder.id_number,
            "name": holder.name,
            "num_insured": holder.insuredperson_set.count(),
            "score": f"{risk_data['score']}% ({risk_data['level']})",
            "patterns": ", ".join(risk_data["explanation"]),
            "timeline": holder.activity_timeline,
        })

    total = high + medium + low or 1
    risk_distribution = {
        "High": round(high / total * 100, 1),
        "Medium": round(medium / total * 100, 1),
        "Low": round(low / total * 100, 1),
    }

    reports.sort(key=lambda x: int(x["score"].split('%')[0]), reverse=True)

    return render(request, "Admin Templates/risk_reports.html", {
        "reports": reports,
        "risk_distribution": risk_distribution
    })


def admin_dashboard(request):
    total_policies = Policy.objects.count()
    active_claims = Claim.objects.filter(status='Pending').count()
    risk_scores = PolicyHolder.objects.aggregate(avg_score=Avg('risk_score'))
    flagged_cases = Claim.objects.filter(status='Flagged').count()  # Adjust as needed
    notifications = Admin_notification.objects.order_by('-created_at')[:5]  # 5 newest notifications
    activity_logs = ActivityLog.objects.order_by('-timestamp')[:10]  # Top 10 logs

    context = {
        'total_policies': total_policies,
        'active_claims': active_claims,
        'risk_scores': risk_scores,
        'flagged_cases': flagged_cases,
        'notifications': notifications,
        'activity_logs': activity_logs,
    }
    return render(request, 'Admin Templates/admin_dashboard.html', context)

def fraud_alerts(request):
    alerts = []

    # 1. High risk policyholders
    high_risk_holders = PolicyHolder.objects.filter(risk_score__gte=80)
    for holder in high_risk_holders:
        alerts.append({
            'alert_type': f'High Risk Score for {holder.name}',
            'severity': 'High',
            'reported_date': date.today(),
            'status': 'Under Review'
        })

    # 2. Suspicious claims: multiple claims in short time
    recent_claims = Claim.objects.filter(dateFiled__gte=date.today() - timedelta(days=60))
    claim_counts = {}
    for claim in recent_claims:
        holder_id = claim.policyHolderId.id_number
        claim_counts[holder_id] = claim_counts.get(holder_id, 0) + 1

    for holder_id, count in claim_counts.items():
        if count >= 3:
            holder = PolicyHolder.objects.get(id_number=holder_id)
            alerts.append({
                'alert_type': f'{count} Claims in 60 Days - {holder.name}',
                'severity': 'Medium',
                'reported_date': date.today(),
                'status': 'Pending'
            })

    # 3. Multiple beneficiaries on one policy
    for policy in Policy.objects.all():
        ben_count = Beneficiary.objects.filter(policy=policy).count()
        if ben_count >= 3:
            alerts.append({
                'alert_type': f'Policy {policy.policyId} has {ben_count} beneficiaries',
                'severity': 'Low',
                'reported_date': date.today(),
                'status': 'Pending'
            })

    # Risk level distribution for chart
    total = len(alerts)
    high = len([a for a in alerts if a['severity'] == 'High'])
    medium = len([a for a in alerts if a['severity'] == 'Medium'])
    low = len([a for a in alerts if a['severity'] == 'Low'])

    def percent(part): return round((part / total) * 100, 1) if total > 0 else 0

    context = {
        'alerts': alerts,
        'high_risk_percent': percent(high),
        'medium_risk_percent': percent(medium),
        'low_risk_percent': percent(low)
    }
    return render(request, 'Admin Templates/fraud_alerts.html', context)

from django.contrib.auth import authenticate, login

from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # First try admin login
        try:
            admin = Admin.objects.get(email=username, password=password)
            request.session['admin_id'] = admin.id
            return redirect('admin_dashboard')
        except Admin.DoesNotExist:
            pass
        
        # Then try regular user authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                # Check policyholder association
                request.user.policyholder
                return redirect('dashboard')
            except PolicyHolder.DoesNotExist:
                messages.error(request, 'No policyholder profile found')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'registration\login.html')

def claim_review(request):
    claims = [
        {
            'claim_id': 'CLM001',
            'policyholder': 'John Doe',
            'beneficiary': 'Jane Doe',
            'risk_score': 'High',
            'status': 'Pending',
            'death_certificate_url': '/static/images/death_certificate1.jpg',
            'timeline': [
                {'event': 'Policy Issued', 'date': '2023-01-01'},
                {'event': 'Insured Died', 'date': '2024-03-15'},
                {'event': 'Claim Filed', 'date': '2024-03-20'},
            ],
            'cause_of_death': 'Cardiac Arrest (Verified)',
        },
        {
            'claim_id': 'CLM002',
            'policyholder': 'Sarah Smith',
            'beneficiary': 'Mark Smith',
            'risk_score': 'Medium',
            'status': 'Pending',
            'death_certificate_url': '/static/images/death_certificate2.jpg',
            'timeline': [
                {'event': 'Policy Issued', 'date': '2022-06-12'},
                {'event': 'Insured Died', 'date': '2023-12-25'},
                {'event': 'Claim Filed', 'date': '2024-01-05'},
            ],
            'cause_of_death': 'Natural Causes (Verified)',
        },
    ]
    return render(request, 'Admin Templates/claim_review.html', {'claims': claims})

def user_management(request):
    return render(request, 'Admin Templates/user_management.html')

#Claim review

from django.shortcuts import render
from .models import PolicyHolder, Claim
from django.http import JsonResponse
from django.template.loader import render_to_string


def claim_review(request):
    query = request.GET.get('search')
    status = request.GET.get('status')
    insured_name = request.GET.get('insured_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    claims = Claim.objects.all()

    if query:
        holders = PolicyHolder.objects.filter(id_number__icontains=query)
        claims = claims.filter(policyHolderId__in=holders)

    if status:
        claims = claims.filter(status__iexact=status)

    if insured_name:
        claims = claims.filter(insured_person__name__icontains=insured_name)

    if start_date:
        claims = claims.filter(claim_date__gte=start_date)
    if end_date:
        claims = claims.filter(claim_date__lte=end_date)

    # AJAX support for dynamic table refresh
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('admin Templates/claim_rows.html', {'claims': claims})
        return JsonResponse({'html': html})

    return render(request, 'admin Templates/claim_review.html', {
         'claims': claims,
         'query': query or '',
         'status': status or '',
         'insured_name': insured_name or '',
         'start_date': start_date or '',
         'end_date': end_date or '',
})

#Policy Review 
from django.db.models import Q


def policy_review(request):
    query = request.GET.get('q', '')
    insured_name = request.GET.get('insured_name', '')
    policy_status = request.GET.get('policy_status', '')
    risk_score = request.GET.get('risk_score', '')

    policies = Policy.objects.all()

    if query:
        policies = policies.filter(
            Q(policyId__icontains=query) |
            Q(policyHolder__name__icontains=query) |
            Q(policyHolder__id_number__icontains=query) |
            Q(policyType__icontains=query) |
            Q(premiumAmount__icontains=query)
        )

    if insured_name:
       policies = policies.filter(insuredperson__name__icontains=insured_name).distinct()

    if policy_status:
        policies = policies.filter(policy_status__iexact=policy_status)

     
       # Add dynamic risk score and filter if needed
    enriched_policies = []
    for policy in policies:
        holder = policy.policyHolder
        risk = assess_policy_risk(holder)
        risk_level = risk['level']
        insured_people = InsuredPerson.objects.filter(policy_id=policy)
        insured_names = ", ".join([person.name for person in insured_people])
        if risk_score and risk_score.lower() != risk_level.lower():
                 continue
    
  
        enriched_policies.append({
            'policy': policy,
            'holder_name': holder.name,
            'risk_score': f"{risk['score']}% ({risk_level})",
            'risk_level': risk_level,
            'explanation': ", ".join(risk['explanation']),
            'insured_names': insured_names,  # 👈 Include this line  
   
            
          })

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
       html = render_to_string('admin Templates/policy_rows.html', {'policies': enriched_policies})
       return JsonResponse({'html': html})

    context = {
        'policies': enriched_policies,  # not the raw queryset
        'query': query,
        'insured_name': insured_name,
        'policy_status': policy_status,
        'risk_score': risk_score,
        
    }
    return render(request, 'Admin Templates/policy_review.html', context)

from django.shortcuts import redirect, get_object_or_404
from .models import Claim  # adjust if in another app

def update_claim_status(request, claim_id):
    if request.method == "POST":
        claim = get_object_or_404(Claim, pk=claim_id)
        new_status = request.POST.get('action')

        if new_status in ['Approved', 'Rejected', 'Investigating']:
            claim.status = new_status
            claim.save()

    return redirect('claim_review')  # Redirect back to claim review page

from django.shortcuts import redirect, get_object_or_404
from .models import Policy  # adjust if in another app

def update_policy_status(request, policy_id):
    if request.method == "POST":
        policy = get_object_or_404(Policy, pk=policy_id)
        new_status = request.POST.get('action')  # Expecting 'Approved' or 'Rejected'

        if new_status in ['Active', 'Cancelled']:
            policy.policy_status = new_status
            policy.save()

    return redirect('policy_review')  # Adjust to match your URL name



from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import PolicyHolder, Policy, Beneficiary, InsuredPerson, Claim
import logging





def policyholder_details(request, id_number):
    try:
        logger.info(f"Fetching details for id_number: {id_number}")
        policyholder = get_object_or_404(PolicyHolder, id_number=id_number)
        data = {
            'name': policyholder.name or 'N/A',
            'id_number': policyholder.id_number,
            'risk_score': policyholder.risk_score if policyholder.risk_score is not None else 'N/A',
            'num_insured': policyholder.insuredperson_set.count(),
            'phone_number': policyholder.phone_number or 'N/A',
            'email': policyholder.email or 'N/A',
            'beneficiary_changes': policyholder.beneficiary_changes or 0,
            'claims_last_year': policyholder.claims_last_year or 0,
            'incomplete_documents': 'Yes' if policyholder.incomplete_documents else 'No',
        }
        logger.info(f"Policyholder details: {data}")
        return JsonResponse(data)
    except PolicyHolder.DoesNotExist:
        logger.error(f"PolicyHolder not found for id_number: {id_number}")
        return JsonResponse({'error': 'Policyholder not found'}, status=404)
    except Exception as e:
        logger.error(f"Error in policyholder_details for id_number {id_number}: {str(e)}")
        return JsonResponse({'error': 'Failed to load details'}, status=500)


def insured_persons_list(request, id_number):
    try:
        policyholder = get_object_or_404(PolicyHolder, id_number=id_number)
        insured_persons = InsuredPerson.objects.filter(holder=policyholder)
        logger.info(f"Found {insured_persons.count()} insured persons for id_number {id_number}")
        data = {
            'insured_persons': [
                {
                    'id': person.id,
                    'name': person.name,
                    'relationship_to_policy_holder': person.relationship_to_policy_holder,
                    'id_number': person.id_number,
                } for person in insured_persons
            ]
        }
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error in insured_persons_list for id_number {id_number}: {e}")
        return JsonResponse({'error': 'Failed to load insured persons'}, status=500)


def insured_person_detail(request, insured_id):
    try:
        person = get_object_or_404(InsuredPerson, id=insured_id)
        data = {
            'name': person.name,
            'date_of_birth': person.date_of_birth.strftime('%Y-%m-%d') if person.date_of_birth else 'N/A',
            'relationship_to_policy_holder': person.relationship_to_policy_holder,
            'id_number': person.id_number,
            'contact_email': person.contact_email or 'N/A',
            'contact_phone': person.contact_phone or 'N/A',
            'parent_id_number': person.parent_id_number or 'N/A',
        }
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error in insured_person_detail for insured_id {insured_id}: {e}")
        return JsonResponse({'error': 'Failed to load insured person details'}, status=500)


def suspicious_patterns(request, id_number):
    try:
        policyholder = get_object_or_404(PolicyHolder, id_number=id_number)
        data = {
            'timeline': policyholder.activity_timeline or []
        }
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error in suspicious_patterns for id_number {id_number}: {e}")
        return JsonResponse({'error': 'Failed to load timeline'}, status=500)


def policyholder_policies(request, id_number):
    try:
        policyholder = get_object_or_404(PolicyHolder, id_number=id_number)
        policies = Policy.objects.filter(policyHolder=policyholder)
        logger.info(f"Found {policies.count()} policies for id_number {id_number}")
        return render(request, 'Admin Templates/policyholder_policies.html', {'policyholder': policyholder, 'policies': policies})
    except Exception as e:
        logger.error(f"Error in policyholder_policies for id_number {id_number}: {e}")
        return render(request, 'Admin Templates/error.html', {'error': 'Failed to load policies'}, status=500)


def policyholder_beneficiaries(request, id_number):
    try:
        policyholder = get_object_or_404(PolicyHolder, id_number=id_number)
        beneficiaries = Beneficiary.objects.filter(policy__policyHolder=policyholder)
        logger.info(f"Found {beneficiaries.count()} beneficiaries for id_number {id_number}")
        return render(request, 'Admin Templates/policyholder_beneficiaries.html', {'policyholder': policyholder, 'beneficiaries': beneficiaries})
    except Exception as e:
        logger.error(f"Error in policyholder_beneficiaries for id_number {id_number}: {e}")
        return render(request, 'Admin Templates/error.html', {'error': 'Failed to load beneficiaries'}, status=500)


def policyholder_insured(request, id_number):
    try:
        policyholder = get_object_or_404(PolicyHolder, id_number=id_number)
        insured_persons = InsuredPerson.objects.filter(holder=policyholder)
        logger.info(f"Found {insured_persons.count()} insured persons for id_number {id_number}")
        return render(request, 'Admin Templates/policyholder_insured.html', {'policyholder': policyholder, 'insured_persons': insured_persons})
    except Exception as e:
        logger.error(f"Error in policyholder_insured for id_number {id_number}: {e}")
        return render(request, 'Admin Templates/error.html', {'error': 'Failed to load insured persons'}, status=500)


def policyholder_claims(request, id_number):
    try:
        policyholder = get_object_or_404(PolicyHolder, id_number=id_number)
        claims = Claim.objects.filter(policyHolderId=policyholder)
        logger.info(f"Found {claims.count()} claims for id_number {id_number}")
        return render(request, 'Admin Templates/policyholder_claims.html', {'policyholder': policyholder, 'claims': claims})
    except Exception as e:
        logger.error(f"Error in policyholder_claims for id_number {id_number}: {e}")
        return render(request, 'Admin Templates/error.html', {'error': 'Failed to load claims'}, status=500)
    

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InsuredPerson, Beneficiary, ActivityLog
from .serializers import InsuredPersonSerializer
from twilio.rest import Client
from django.conf import settings

class UpdateInsuredStatus(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            insured = InsuredPerson.objects.get(pk=pk)
        except InsuredPerson.DoesNotExist:
            return Response({'error': 'Insured person not found'}, status=status.HTTP_404_NOT_FOUND)

        if insured.status == 'deceased':
            return Response({'message': 'Insured person is already deceased'}, status=status.HTTP_400_BAD_REQUEST)

        insured.status = 'deceased'
        insured.save()

        # Notify beneficiaries and log the action
        self.notify_beneficiaries(insured)
        self.log_activity(request.user, insured)

        return Response({'message': 'Status updated to deceased'}, status=status.HTTP_200_OK)

    def notify_beneficiaries(self, insured):
        policy = insured.policy_id
        beneficiaries = Beneficiary.objects.filter(policy=policy)
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        for beneficiary in beneficiaries:
            message = "The insured person has been declared deceased. You can now file a claim."
            client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=beneficiary.contactNumber  # Must be in format like '+1234567890'
            )

    def log_activity(self, user, insured):
        """Log the status update in ActivityLog."""
        ActivityLog.objects.create(
            user=user.username,
            action='Updated insured person status',
            details=f'Set status to deceased for insured person {insured.id}'
        )

@login_required(login_url='login')
def profile(request):
    adminholder = Admin.objects.filter(user=request.user).first()

    context = {
        'adminholder': adminholder,
    }
    return render(request, 'Admin Templates/profile.html', context)
        
def AdminNotis(request):
    return redirect('Admin Templates/notifications.html') 

#Beneficiary Login
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Beneficiary
import random
from django.urls import reverse

def login_request(request):
    if request.method == 'POST':
        beneficiary_id = request.POST['beneficiaryId']
        email = request.POST['email']

        try:
            Beneficiary.objects.get(beneficiaryId=int(beneficiary_id.strip()),email__iexact=email.strip()
)
            otp = str(random.randint(100000, 999999))

            # Store OTP and email in session
            request.session['otp'] = otp
            request.session['email'] = email

            # Send OTP to email
            send_mail(
                'Your Login OTP',
                f'Your OTP is {otp}',
                'no-reply@insurance.com',
                [email]
            )
            return render(request, 'Beneficiary/enter_otp.html', {'email': email})
        except Beneficiary.DoesNotExist:
            return render(request, 'Beneficiary/beneficiaryLogin.html', {'error': 'Invalid credentials'})

    return render(request, 'Beneficiary/beneficiaryLogin.html')


def verify_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp_input = request.POST['otp']

        stored_otp = request.session.get('otp')
        stored_email = request.session.get('email')

        if stored_otp == otp_input and stored_email == email:
            try:
                beneficiary = Beneficiary.objects.get(email=email)
                request.session['beneficiary_id'] = beneficiary.beneficiaryId
                return redirect('beneficiary_dashboard')
            except Beneficiary.DoesNotExist:
                return render(request, 'Beneficiary/enter_otp.html', {'email': email, 'error': 'Beneficiary not found'})
        else:
            return render(request, 'Beneficiary/enter_otp.html', {'email': email, 'error': 'Incorrect OTP'})

    # For GET requests
    email = request.GET.get('email')
    return render(request, 'Beneficiary/enter_otp.html', {'email': email})


def resend_otp(request):
    email = request.GET.get('email')

    if not email:
        return redirect('login')

    otp = str(random.randint(100000, 999999))
    request.session['otp'] = otp
    request.session['email'] = email

    send_mail(
        'Your OTP Code',
        f'Your new OTP is {otp}',
        'noreply@ifp.com',
        [email],
        fail_silently=False,
    )

    return redirect(f"{reverse('enter_otp')}?email={email}")


def beneficiary_login(request):
    return render(request, 'Beneficiary/beneficiaryLogin.html')





from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Claim, Policy, Beneficiary, PolicyHolder

def file_claim(request):
    if request.method == 'POST':
        # Get beneficiary from session (set during OTP login)
        beneficiary_id = request.session.get('beneficiary_id')
        if not beneficiary_id:
            messages.error(request, "You must be logged in to submit a claim.")
            return redirect('beneficiary_login')

        # Extract form data
        policy_id = request.POST.get('policyId')
        selected_beneficiary_id = request.POST.get('beneficiaryId')
        id_number = request.POST.get('id_number')
        claim_amount = request.POST.get('claimAmount')

        # Ensure the selected beneficiary matches the logged-in user
        if str(beneficiary_id) != selected_beneficiary_id:
            messages.error(request, "You are not allowed to file a claim for another beneficiary.")
            return redirect('claim_form')

        try:
            policy = Policy.objects.get(policyId=policy_id)
            beneficiary = Beneficiary.objects.get(beneficiaryId=beneficiary_id)
            policy_holder = PolicyHolder.objects.get(id_number=id_number)

            # Create the claim
            Claim.objects.create(
                policy=policy,
                beneficiary=beneficiary,
                policy_holder=policy_holder,
                claim_amount=claim_amount,
                status='Pending'
            )

            messages.success(request, "Claim submitted successfully.")
            return redirect('beneficiary_dashboard')
        except (Policy.DoesNotExist, Beneficiary.DoesNotExist, PolicyHolder.DoesNotExist):
            messages.error(request, "Invalid data. Please check your selections.")
            return redirect('claim_form')

    # If GET, redirect to form
    return redirect('claim_form')

def claim_form(request):
    beneficiary_id = request.session.get('beneficiary_id')
    if not beneficiary_id:
        return redirect('beneficiary_login')

    # Get logged-in beneficiary
    beneficiary = get_object_or_404(Beneficiary, beneficiaryId=beneficiary_id)

    if request.method == 'POST':
        policy_id = request.POST.get('policyId')
        id_number = request.POST.get('id_number')
        claim_amount = request.POST.get('claimAmount')

        # Validate input existence
        if not (policy_id and id_number and claim_amount):
            messages.error(request, "Please fill in all required fields.")
            return redirect('claim_form')

        try:
            # Fetch related objects to link in Claim
            policy = Policy.objects.get(policyId=policy_id)
            policy_holder = PolicyHolder.objects.get(id_number=id_number)

            # Security: Check that this beneficiary is linked to the policy
            if beneficiary.policy.policyId != policy.policyId:
                messages.error(request, "You can only claim on your own policies.")
                return redirect('claim_form')

            # Check that the policy_holder matches the policy's policyHolder
            if policy.policyHolder != policy_holder:
                messages.error(request, "Policy holder does not match the selected policy.")
                return redirect('claim_form')

            # Create Claim
            new_claim = Claim.objects.create(
                policyId=policy,
                beneficiaryId=beneficiary,
                policyHolderId=policy_holder,
                claimAmount=claim_amount,
                status='Pending Fraud Check'
            )

            messages.success(request, "Claim submitted successfully.")
            return redirect('beneficiary_dashboard')

        except Policy.DoesNotExist:
            messages.error(request, "Selected policy does not exist.")
        except PolicyHolder.DoesNotExist:
            messages.error(request, "Selected policy holder does not exist.")
        except Exception as e:
            messages.error(request, f"Error submitting claim: {e}")

    # GET: show policies linked to this beneficiary and related policyholders
    # Since Beneficiary has a ForeignKey to Policy, get that Policy
    policy = beneficiary.policy
    policyholders = PolicyHolder.objects.filter(id_number=policy.policyHolder.id_number)

    return render(request, 'Beneficiary/claim_form.html', {
        'policies': [policy],            # Single policy linked to beneficiary
        'beneficiaries': [beneficiary], # Only the logged-in beneficiary
        'policyholders': policyholders,
    })

def claim_details(request):
    beneficiary_id = request.session.get('beneficiary_id')

    if not beneficiary_id:
        return redirect('beneficiary_login')  # replace with your login route name

    beneficiary = Beneficiary.objects.filter(beneficiaryId=beneficiary_id).first()

    if not beneficiary:
        return render(request, 'Beneficiary/claim_details.html', {'error': 'No beneficiary found for your account.'})

    claims = Claim.objects.filter(beneficiaryId=beneficiary).order_by('-dateFiled')

    return render(request, 'Beneficiary/claim_details.html', {'claims': claims})

def support_panel(request):
    return render(request, 'Beneficiary/support_panel.html')

def appeals_history(request):
    return render(request, 'Beneficiary/appeals_history.html')       