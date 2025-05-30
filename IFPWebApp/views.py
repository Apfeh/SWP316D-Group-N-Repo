from django.shortcuts import render, redirect, get_object_or_404
from .models import Beneficiary
from .forms import BeneficiaryForm
from .models import Claim
from .forms import ClaimForm
from .models import InsuredPerson
from .models import Notification,ActivityLog
from django.urls import reverse
from .models import PolicyHolder
from .models import Admin
from django.http import HttpResponseNotAllowed
from django.http import HttpResponse
from django.contrib import messages
from .models import FraudPreventionTeam,Policy
from django.contrib.auth.hashers import make_password





def login_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        email = request.POST.get('username')
        password = request.POST.get('password')

        if role == 'admin':
            try:
                admin = Admin.objects.get(email=email, password=password)
                request.session['admin_id'] = admin.id
                return redirect('admin_dashboard')
            except Admin.DoesNotExist:
                return render(request, 'login.html', {'error': 'Invalid Admin credentials'})

        elif role == 'policy_holder':
            try:
                holder = PolicyHolder.objects.get(email=email, password=password)
                return render(request, 'Policyholder Pages/dashboard.html', {'holder': holder})
            except PolicyHolder.DoesNotExist:
                return render(request, 'login.html', {'error': 'Invalid Policy Holder credentials'})

    return render(request, 'login.html')

def landing_page(request):
    return render(request, 'landing_page.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')


def beneficiary_list(request):
    beneficiaries = Beneficiary.objects.all()
    return render(request, 'beneficiary_list.html', {'beneficiaries': beneficiaries})

def beneficiary_create(request):
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_list')
    else:
        form = BeneficiaryForm()
    return render(request, 'beneficiary_form.html', {'form': form})

def beneficiary_update(request, id):
    beneficiary = get_object_or_404(Beneficiary, pk=id)
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST, instance=beneficiary)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_list')
    else:
        form = BeneficiaryForm(instance=beneficiary)
    return render(request, 'beneficiary_form.html', {'form': form})

def beneficiary_delete(request, id):
    beneficiary = get_object_or_404(Beneficiary, pk=id)
    if request.method == 'POST':
        beneficiary.delete()
        return redirect('beneficiary_list')
    return render(request, 'beneficiary_confirm_delete.html', {'beneficiary': beneficiary})

#Claims View
def claim(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim_instance = form.save(commit=False)
            claim_instance.status = 'pending'
            claim_instance.save()
            form = ClaimForm()
    else:
        form = ClaimForm()
    
    claims = Claim.objects.all().order_by('-dateFiled')
    for c in claims:
        print(f"Claim: {c.claimId}, {c.policyId}, {c.status}, {c.dateFiled}")  # Debug print
    return render(request, 'claim.html', {'form': form, 'claims': claims})

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


from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from .models import FraudPreventionTeam, Claim, Policy
import logging

# Set up logging
logger = logging.getLogger(__name__)

def manage_team(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        logger.debug(f"POST data: {request.POST}")  # Log POST data for debugging

        if action == 'add':
            try:
                claim = Claim.objects.get(pk=request.POST.get('claimid'))
                policy = Policy.objects.get(pk=request.POST.get('policyid'))
                FraudPreventionTeam.objects.create(
                    claimid=claim,
                    policyid=policy,
                    contactNumber=request.POST.get('contactNumber'),
                    department=request.POST.get('department'),
                    investigatorName=request.POST.get('investigatorName')
                )
                messages.success(request, 'Team member added successfully.')
            except Claim.DoesNotExist:
                messages.error(request, 'Claim not found.')
            except Policy.DoesNotExist:
                messages.error(request, 'Policy not found.')
            except Exception as e:
                logger.error(f"Error adding team member: {e}")
                messages.error(request, f'Error adding team member: {e}')

        elif action == 'update':
            try:
                teamid = request.POST.get('teamid')
                member = FraudPreventionTeam.objects.get(teamid=teamid)
                claim = Claim.objects.get(pk=request.POST.get('claimid'))
                policy = Policy.objects.get(pk=request.POST.get('policyid'))
                member.claimid = claim
                member.policyid = policy
                member.contactNumber = request.POST.get('contactNumber')
                member.department = request.POST.get('department')
                member.investigatorName = request.POST.get('investigatorName')
                member.save()
                messages.success(request, 'Team member updated successfully.')
            except FraudPreventionTeam.DoesNotExist:
                messages.error(request, 'Team member not found.')
            except Claim.DoesNotExist:
                messages.error(request, 'Claim not found.')
            except Policy.DoesNotExist:
                messages.error(request, 'Policy not found.')
            except Exception as e:
                logger.error(f"Error updating team member: {e}")
                messages.error(request, f'Error updating team member: {e}')

        elif action == 'delete':
            try:
                teamid = request.POST.get('teamid')
                if not teamid:
                    raise ValueError("Team ID is missing.")
                member = FraudPreventionTeam.objects.get(teamid=teamid)
                member.delete()
                messages.success(request, 'Team member removed successfully.')
            except FraudPreventionTeam.DoesNotExist:
                messages.error(request, f'Team member with ID {teamid} not found.')
            except ValueError as ve:
                messages.error(request, str(ve))
            except Exception as e:
                logger.error(f"Error removing team member with ID {teamid}: {e}")
                messages.error(request, f'Error removing team member: {e}')

        return redirect('manage_team')

    elif request.method == 'GET':
        team_members = FraudPreventionTeam.objects.select_related('claimid', 'policyid').all()
        return render(request, 'fraud_prevention.html', {'team_members': team_members})

    return HttpResponseNotAllowed(['GET', 'POST'])

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

from django.shortcuts import render, redirect
from datetime import date, datetime, timedelta

# ---- Admin Dashboard View ----
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
    return render(request, 'Admin Templates/admin_dashboard.html', context)

# ---- Home Page ----
def home(request):
    return render(request, 'boitshepo/home.html')

# ---- Dummy Policies ----
POLICIES = [
    {'id': 1, 'holder_name': 'John Doe', 'insured_persons': 'Jane Doe', 'risk_score': 75, 'status': 'Pending'},
    {'id': 2, 'holder_name': 'Alice Smith', 'insured_persons': 'Bob Smith', 'risk_score': 55, 'status': 'Pending'},
    {'id': 3, 'holder_name': 'Mark Johnson', 'insured_persons': 'Lucy Johnson', 'risk_score': 85, 'status': 'Pending'},
]

# ---- Policy Review ----
def policy_review(request):
    query = request.GET.get('q', '')
    filtered_policies = [policy for policy in POLICIES if query.lower() in policy['holder_name'].lower()]
    context = {'policies': filtered_policies}
    return render(request, 'Admin Templates/policy_review.html', context)

def policy_detail(request, pk):
    selected_policy = next((policy for policy in POLICIES if policy['id'] == pk), None)
    if not selected_policy:
        return redirect('policy_review')
    context = {'selected_policy': selected_policy}
    return render(request, 'Admin Templates/policy_review.html', context)

def approve_policy(request, pk):
    policy = next((policy for policy in POLICIES if policy['id'] == pk), None)
    if policy:
        policy['status'] = 'Approved'
    return redirect('policy_review')

def reject_policy(request, pk):
    policy = next((policy for policy in POLICIES if policy['id'] == pk), None)
    if policy:
        policy['status'] = 'Rejected'
    return redirect('policy_review')

# ---- Claim Review ----
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

# ---- Fraud Alerts ----
def fraud_alerts(request):
    alerts = [
        {
            'timestamp': '2025-04-26 12:34:56',
            'user': 'John Doe',
            'type': 'Anomaly Detected',
            'severity': 'Critical',
        },
        {
            'timestamp': '2025-04-26 13:22:10',
            'user': 'Jane Smith',
            'type': 'Death Pattern Match',
            'severity': 'Medium',
        },
        {
            'timestamp': '2025-04-26 14:45:30',
            'user': 'Alice Johnson',
            'type': 'Unusual Claim Spike',
            'severity': 'Low',
        },
    ]
    return render(request, 'Admin Templates/fraud_alerts.html', {'alerts': alerts})

# ---- User Management ----
def user_management(request):
    return render(request, 'Admin Templates/user_management.html')

def dashboard(request):
    context = {
        'active_policies': 3,
        'pending_claims': 1,
        'notifications': 2,
    }
    return render(request, 'Policyholder Pages/dashboard.html', context)

def add_policy(request):
    if request.method == 'POST':
        # Placeholder: Process form data (e.g., save to database)
        messages.success(request, 'Policy submitted successfully!')
        return redirect('policy_status')
    return render(request, 'Policyholder Pages/add-policy.html')

def policy_status(request):
    # Fake policy data
    policies = [
        {'id': 'POL001', 'insured_name': 'John Doe', 'status': 'Pending', 'details': 'Awaiting insured consent'},
        {'id': 'POL002', 'insured_name': 'Jane Smith', 'status': 'Approved', 'details': 'Policy active'},
        {'id': 'POL003', 'insured_name': 'Mary Johnson', 'status': 'Rejected', 'details': 'Invalid documents'},
    ]
    context = {'policies': policies}
    return render(request, 'Policyholder Pages/policy-status.html', context)

def manage_beneficiaries(request):
    # Fake beneficiary data
    beneficiaries = [
        {'policy_id': 'POL001', 'name': 'Sarah Lee', 'contact': 'sarah@example.com'},
    ]
    # Fake policy options for form
    policy_options = [
        {'id': 'POL001', 'name': 'John Doe'},
        {'id': 'POL002', 'name': 'Jane Smith'},
    ]
    if request.method == 'POST':
        # Placeholder: Process beneficiary form data
        messages.success(request, 'Beneficiary added successfully!')
        return redirect('manage_beneficiaries')
    context = {'beneficiaries': beneficiaries, 'policy_options': policy_options}
    return render(request, 'Policyholder Pages/manage-beneficiaries.html', context)

def file_claim(request):
    # Fake policy options for form
    policy_options = [
        {'id': 'POL001', 'name': 'John Doe'},
        {'id': 'POL002', 'name': 'Jane Smith'},
    ]
    if request.method == 'POST':
        # Placeholder: Process claim form data
        messages.success(request, 'Claim submitted successfully!')
        return redirect('claim_status')
    context = {'policy_options': policy_options}
    return render(request, 'Policyholder Pages/file-claim.html', context)

def claim_status(request):
    # Fake claim data
    claims = [
        {'id': 'CLM001', 'policy_id': 'POL001', 'status': 'Pending', 'details': 'Under investigation'},
        {'id': 'CLM002', 'policy_id': 'POL002', 'status': 'Approved', 'details': 'Payout processed'},
        {'id': 'CLM003', 'policy_id': 'POL003', 'status': 'Rejected', 'details': 'Suspicious activity detected'},
    ]
    context = {'claims': claims}
    return render(request, 'Policyholder Pages/claim-status.html', context)

def index(request):
    # Placeholder: Redirect to landing page or handle logout
    return redirect('dashboard')  # Temporary redirect for testing
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseNotAllowed, HttpResponse
from django.contrib import messages
from .models import Beneficiary, Claim, InsuredPerson, PolicyHolder, FraudPreventionTeam, Policy
from .forms import BeneficiaryForm, ClaimForm
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

# Landing and Authentication

def landing_page(request):
    return render(request, 'landing_page.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

# Beneficiary Views

def beneficiary_list(request):
    beneficiaries = Beneficiary.objects.all()
    return render(request, 'beneficiary_list.html', {'beneficiaries': beneficiaries})

def beneficiary_create(request):
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_list')
    else:
        form = BeneficiaryForm()
    return render(request, 'beneficiary_form.html', {'form': form})

def beneficiary_update(request, id):
    beneficiary = get_object_or_404(Beneficiary, pk=id)
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST, instance=beneficiary)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_list')
    else:
        form = BeneficiaryForm(instance=beneficiary)
    return render(request, 'beneficiary_form.html', {'form': form})

def beneficiary_delete(request, id):
    beneficiary = get_object_or_404(Beneficiary, pk=id)
    if request.method == 'POST':
        beneficiary.delete()
        return redirect('beneficiary_list')
    return render(request, 'beneficiary_confirm_delete.html', {'beneficiary': beneficiary})

# Claims View

def claim(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim_instance = form.save(commit=False)
            claim_instance.status = 'pending'
            claim_instance.save()
            form = ClaimForm()
    else:
        form = ClaimForm()

    claims = Claim.objects.all().order_by('-dateFiled')
    return render(request, 'claim.html', {'form': form, 'claims': claims})

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

# Fraud Prevention Team View

def manage_team(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        logger.debug(f"POST data: {request.POST}")

        if action == 'add':
            try:
                claim = Claim.objects.get(pk=request.POST.get('claimid'))
                policy = Policy.objects.get(pk=request.POST.get('policyid'))
                FraudPreventionTeam.objects.create(
                    claimid=claim,
                    policyid=policy,
                    contactNumber=request.POST.get('contactNumber'),
                    department=request.POST.get('department'),
                    investigatorName=request.POST.get('investigatorName')
                )
                messages.success(request, 'Team member added successfully.')
            except Exception as e:
                logger.error(f"Error adding team member: {e}")
                messages.error(request, f'Error adding team member: {e}')

        elif action == 'update':
            try:
                teamid = request.POST.get('teamid')
                member = FraudPreventionTeam.objects.get(teamid=teamid)
                member.claimid = Claim.objects.get(pk=request.POST.get('claimid'))
                member.policyid = Policy.objects.get(pk=request.POST.get('policyid'))
                member.contactNumber = request.POST.get('contactNumber')
                member.department = request.POST.get('department')
                member.investigatorName = request.POST.get('investigatorName')
                member.save()
                messages.success(request, 'Team member updated successfully.')
            except Exception as e:
                logger.error(f"Error updating team member: {e}")
                messages.error(request, f'Error updating team member: {e}')

        elif action == 'delete':
            try:
                teamid = request.POST.get('teamid')
                member = FraudPreventionTeam.objects.get(teamid=teamid)
                member.delete()
                messages.success(request, 'Team member removed successfully.')
            except Exception as e:
                logger.error(f"Error removing team member: {e}")
                messages.error(request, f'Error removing team member: {e}')

        return redirect('manage_team')

    elif request.method == 'GET':
        team_members = FraudPreventionTeam.objects.select_related('claimid', 'policyid').all()
        return render(request, 'fraud_prevention.html', {'team_members': team_members})

    return HttpResponseNotAllowed(['GET', 'POST'])

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
    return render(request, 'Admin Templates/admin_dashboard.html', context)

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



# reviews


def policy_review(request):
    query = request.GET.get('q', '')
    if query:
        policies = Policy.objects.filter(policyHolder_name_icontains=query)
    else:
        policies = Policy.objects.all()
    context = {'policies': policies}
    return render(request, 'policy_review.html', context)

def policy_detail(request, pk):
    policy = get_object_or_404(Policy, pk=pk)
    insured_persons = InsuredPerson.objects.filter(policy=policy)
    context = {'selected_policy': policy, 'insured_persons': insured_persons}
    return render(request, 'policy_detail.html', context)

def approve_policy(request, pk):
    policy = get_object_or_404(Policy, pk=pk)
    policy.status = 'Approved'
    policy.save()
    return redirect('policy_review')

def reject_policy(request, pk):
    policy = get_object_or_404(Policy, pk=pk)
    policy.status = 'Rejected'
    policy.save()
    return redirect('policy_review')



#Risk Reports

from django.shortcuts import render
from .ai_engine import assess_policy_risk
from .models import PolicyHolder

def risk_reports(request):
    reports = []
    policyholders = PolicyHolder.objects.all()
    print("PolicyHolders Count:", policyholders.count())


    # Risk distribution counters
    high = medium = low = 0

    for holder in policyholders:
        risk_data = assess_policy_risk(holder)

        holder.risk_score= risk_data["score"]
        holder.save(update_fields=['risk_score'])

        if risk_data["level"] == "High":
            high += 1
        elif risk_data["level"] == "Medium":
            medium += 1
        else:
            low += 1

        reports.append({
            "name": holder.name,
            "num_insured": holder.insuredperson_set.count(),
            "score": f"{risk_data['score']}% ({risk_data['level']})",
            "patterns": ", ".join(risk_data["explanation"]),
            "timeline": holder.activity_timeline,
        })

    total = high + medium + low or 1  # Avoid division by zero

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




def logout_view(request):
    # Clear the session (or any login state)
    request.session.flush()
    return redirect('login') # Redirect to login page after logout

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Policy, Claim  # Replace with actual model names
from django.db.models import Avg

#@login_required
def admin_dashboard(request):
    if 'admin_id' not in request.session:
        return redirect('login')

    total_policies = Policy.objects.count()
    active_claims = Claim.objects.filter(status='active').count()
    risk_scores = PolicyHolder.objects.aggregate(avg_score=Avg('risk_score'))
    notifications = Notification.objects.all()[:5]
    activity_logs = ActivityLog.objects.all()[:10]  # Assuming ActivityLog exists

    context = {
        'total_policies': total_policies,
        'active_claims': active_claims,
        'risk_scores': risk_scores,
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
