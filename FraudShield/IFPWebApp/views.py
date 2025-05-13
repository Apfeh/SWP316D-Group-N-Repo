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
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')


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
    return render(request, 'dashboard.html')

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
def dashboard(request):
    return render(request, 'dashboard.html')

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


# Main dashboard
def dashboard(request):
    return render(request, 'dashboard.html')


# Dalphy's Beneficiary Pages
def add_beneficiary(request):
    return render(request, "add_beneficiary.html")

def beneficiary_dashboard(request):
    return render(request, "beneficiary_dashboard.html")

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
    return render(request, 'landing_page.html')

def login(request):
    return render(request, 'login.html')

#def register(request):
   # return render(request, 'registration/register.html')

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

def dashboard(request):
    return render(request, 'dashboard.html')

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

def beneficiary_dashboard(request):
    return render(request, "beneficiary_dashboard.html")

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

def admin_dashboard(request):
    context = {
        'total_policies': 120,
        'active_claims': 42,
        'flagged_cases': 5,
        'risk_scores': 78,
        'notifications': [
            "New claim filed by Policy #7789",
            "Policy #4567 flagged for manual review",
            "System maintenance scheduled at 10PM"
        ],
    }
    return render(request, 'boitshepo/admin_dashboard.html', context)

def home(request):
    return render(request, 'boitshepo/home.html')

POLICIES = [
    {'id': 1, 'holder_name': 'John Doe', 'insured_persons': 'Jane Doe', 'risk_score': 75, 'status': 'Pending'},
    {'id': 2, 'holder_name': 'Alice Smith', 'insured_persons': 'Bob Smith', 'risk_score': 55, 'status': 'Pending'},
    {'id': 3, 'holder_name': 'Mark Johnson', 'insured_persons': 'Lucy Johnson', 'risk_score': 85, 'status': 'Pending'},
]

def policy_review(request):
    query = request.GET.get('q', '')
    filtered_policies = [policy for policy in POLICIES if query.lower() in policy['holder_name'].lower()]
    context = {'policies': filtered_policies}
    return render(request, 'policy_review.html', context)


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
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in. Redirected to dashboard.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
        else:
            logger.debug(f"Form errors: {form.errors}")
            messages.error(request, 'Registration failed. Please check the form.')
    else:
        form = CustomRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def landing_page(request):
    return render(request, 'landing_page.html')

@login_required
def log_register(request):
    messages.warning(request, 'You are already logged in. Redirected to dashboard.')
    return redirect('dashboard')

@login_required
def dashboard(request):
    logger.debug(f"User email: {request.user.email}")
    try:
        policy_holder = PolicyHolder.objects.get(email=request.user.email)
        logger.debug(f"Found PolicyHolder: {policy_holder.idno}")
        active_policies = Policy.objects.filter(policyHolder=policy_holder).count()
        pending_claims = Claim.objects.filter(policy__policyHolder=policy_holder, status='Pending').count()
        notifications = pending_claims  # Notifications based on pending claims
        name = policy_holder.name
    except PolicyHolder.DoesNotExist:
        logger.warning(f"No PolicyHolder found for email: {request.user.email}")
        active_policies = 0
        pending_claims = 0
        notifications = 0
        name = "User"
        messages.error(request, f'No policyholder profile found for email: {request.user.email}. Please contact support.')
    context = {
        'active_policies': active_policies,
        'pending_claims': pending_claims,
        'notifications': notifications,
        'name': name,
    }
    return render(request, 'Policyholder Pages/dashboard.html', context)

@login_required
def notifications(request):
    logger.debug(f"User email: {request.user.email}")
    try:
        policy_holder = PolicyHolder.objects.get(email=request.user.email)
        logger.debug(f"Found PolicyHolder: {policy_holder.idno}")
        pending_claims = Claim.objects.filter(policy__policyHolder=policy_holder, status='Pending')
        logger.debug(f"Found {pending_claims.count()} pending claims for PolicyHolder: {policy_holder.idno}")
    except PolicyHolder.DoesNotExist:
        logger.warning(f"No PolicyHolder found for email: {request.user.email}")
        pending_claims = []
        messages.error(request, 'No policyholder profile found. Please contact support.')
    context = {
        'pending_claims': pending_claims,
    }
    return render(request, 'Policyholder Pages/notifications.html', context)

@login_required
def add_policy(request):
    logger.debug(f"User email: {request.user.email}")
    try:
        policy_holder = PolicyHolder.objects.get(email=request.user.email)
        logger.debug(f"Found PolicyHolder: {policy_holder.email}")
    except PolicyHolder.DoesNotExist:
        logger.warning(f"No PolicyHolder found for email: {request.user.email}")
        messages.error(request, 'No policyholder profile found. Please contact support.')
        return redirect('dashboard')

    if request.method == 'POST':
        insured_name = request.POST.get('insured_name')
        insured_contact = request.POST.get('insured_contact')
        policy_type = request.POST.get('policy_type')
        relationship_docs = request.FILES.get('relationship_docs')

        policy = Policy(
            policyHolder=policy_holder,
            policyType=policy_type,
            premiumAmount=0.00,
            startDate='2025-01-01',
            endDate='2026-01-01'
        )
        policy.save()

        insured_person = InsuredPerson(
            policy=policy,
            name=insured_name,
            dateOfBirth='1970-01-01',
            relationshipToPolicyHolder='Self'
        )
        insured_person.save()

        if relationship_docs:
            fs = FileSystemStorage()
            filename = fs.save(relationship_docs.name, relationship_docs)
        
        messages.success(request, 'Policy added successfully!')
        return redirect('dashboard')

    return render(request, 'Policyholder Pages/add-policy.html')

@login_required
def policy_status(request):
    logger.debug(f"User email: {request.user.email}")
    try:
        policy_holder = PolicyHolder.objects.get(email=request.user.email)
        logger.debug(f"Found PolicyHolder: {policy_holder.email}")
        policies = Policy.objects.filter(policyHolder=policy_holder)
        logger.debug(f"Found {policies.count()} policies for PolicyHolder: {policy_holder.email}")
    except PolicyHolder.DoesNotExist:
        logger.warning(f"No PolicyHolder found for email: {request.user.email}")
        messages.error(request, 'No policyholder profile found. Please contact support.')
        return redirect('dashboard')
    context = {
        'policies': policies,
    }
    return render(request, 'Policyholder Pages/policy-status.html', context)

@login_required
def manage_beneficiaries(request):
    logger.debug(f"User email: {request.user.email}")
    try:
        policy_holder = PolicyHolder.objects.get(email=request.user.email)
        logger.debug(f"Found PolicyHolder: {policy_holder.email}")
    except PolicyHolder.DoesNotExist:
        logger.warning(f"No PolicyHolder found for email: {request.user.email}")
        messages.error(request, 'No policyholder profile found. Please contact support.')
        return redirect('dashboard')

    if request.method == 'POST':
        policy_id = request.POST.get('policy_id')
        beneficiary_name = request.POST.get('beneficiary_name')
        beneficiary_contact = request.POST.get('beneficiary_contact')
        relationship = request.POST.get('relationship')

        try:
            policy = Policy.objects.get(policyID=policy_id, policyHolder=policy_holder)
            beneficiary = Beneficiary(
                policy=policy,
                name=beneficiary_name,
                contactNumber=beneficiary_contact,
                relationshipToInsured=relationship
            )
            beneficiary.save()
            messages.success(request, 'Beneficiary added successfully!')
        except Policy.DoesNotExist:
            messages.error(request, 'Selected policy not found.')
        return redirect('manage_beneficiaries')

    policy_options = Policy.objects.filter(policyHolder=policy_holder)
    beneficiaries = Beneficiary.objects.filter(policy__policyHolder=policy_holder)
    logger.debug(f"Found {policy_options.count()} policy options, {beneficiaries.count()} beneficiaries for PolicyHolder: {policy_holder.email}")
    context = {
        'policy_options': policy_options,
        'beneficiaries': beneficiaries,
    }
    return render(request, 'Policyholder Pages/manage-beneficiaries.html', context)

@login_required
def file_claim(request):
    logger.debug(f"User email: {request.user.email}")
    try:
        policy_holder = PolicyHolder.objects.get(email=request.user.email)
        logger.debug(f"Found PolicyHolder: {policy_holder.email}")
    except PolicyHolder.DoesNotExist:
        logger.warning(f"No PolicyHolder found for email: {request.user.email}")
        messages.error(request, 'No policyholder profile found. Please contact support.')
        return redirect('dashboard')

    if request.method == 'POST':
        policy_id = request.POST.get('policy_id')
        death_certificate = request.FILES.get('death_certificate')
        cause_of_death = request.POST.get('cause_of_death')

        try:
            policy = Policy.objects.get(policyID=policy_id, policyHolder=policy_holder)
            beneficiary = Beneficiary.objects.filter(policy=policy).first()
            if not beneficiary:
                messages.error(request, 'No beneficiary found for this policy.')
                return redirect('file_claim')

            claim = Claim(
                policy=policy,
                beneficiary=beneficiary,
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
    logger.debug(f"Found {policy_options.count()} policy options for PolicyHolder: {policy_holder.email}")
    context = {
        'policy_options': policy_options,
    }
    return render(request, 'Policyholder Pages/file-claim.html', context)

@login_required
def claim_status(request):
    logger.debug(f"User email: {request.user.email}")
    try:
        policy_holder = PolicyHolder.objects.get(email=request.user.email)
        logger.debug(f"Found PolicyHolder: {policy_holder.email}")
        claims = Claim.objects.filter(policy__policyHolder=policy_holder)
        logger.debug(f"Found {claims.count()} claims for PolicyHolder: {policy_holder.email}")
    except PolicyHolder.DoesNotExist:
        logger.warning(f"No PolicyHolder found for email: {request.user.email}")
        messages.error(request, 'No policyholder profile found. Please contact support.')
        return redirect('dashboard')
    context = {
        'claims': claims,
    }
    return render(request, 'Policyholder Pages/claim-status.html', context)