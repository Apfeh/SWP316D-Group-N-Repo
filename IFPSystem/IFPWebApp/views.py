from django.shortcuts import render, redirect, get_object_or_404
from .models import Beneficiary
from .forms import BeneficiaryForm
from .models import Claim
from .forms import ClaimForm
from .models import InsuredPerson
from django.urls import reverse
from .models import PolicyHolder
from django.http import HttpResponse
from django.contrib import messages
from .models import TeamMember

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
            form.save()
            form = ClaimForm()  # Reset form after successful submission
    else:
        form = ClaimForm()
    
    claims = Claim.objects.all().order_by('-dateFiled')
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
        PolicyHolder.objects.create(
            policyHolderId=policyHolderId,
            name=name,
            address=address,
            contact=contact,
            email=email
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


#FraudTeam
def manage_team(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            try:
                TeamMember.objects.create(
                    claimid=request.POST['claimid'],
                    policyid=request.POST['policyid'],
                    contactNumber=request.POST['contactNumber'],
                    department=request.POST['department'],
                    investigatorName=request.POST['investigatorName']
                )
                messages.success(request, 'Team member added successfully.')
            except Exception as e:
                messages.error(request, f'Error adding team member: {e}')
        elif action == 'update':
            try:
                teamid = request.POST['teamid']
                member = TeamMember.objects.get(teamid=teamid)
                member.claimid = request.POST['claimid']
                member.policyid = request.POST['policyid']
                member.contactNumber = request.POST['contactNumber']
                member.department = request.POST['department']
                member.investigatorName = request.POST['investigatorName']
                member.save()
                messages.success(request, 'Team member updated successfully.')
            except TeamMember.DoesNotExist:
                messages.error(request, 'Team member not found.')
            except Exception as e:
                messages.error(request, f'Error updating team member: {e}')
        elif action == 'delete':
            try:
                teamid = request.POST.get('teamid')
                member = TeamMember.objects.get(teamid=teamid)
                member.delete()
                messages.success(request, 'Team member removed successfully.')
            except TeamMember.DoesNotExist:
                messages.error(request, 'Team member not found.')
            except Exception as e:
                messages.error(request, f'Error removing team member: {e}')
        return redirect('manage_team')
    
    # GET request: Render the template with team members
    team_members = TeamMember.objects.all()
    return render(request, 'fraud_prevention.html', {'team_members': team_members})