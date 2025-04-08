# main/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'base.html')  # Your homepage (you can create this page)

def manage_policyholders(request):
    return render(request, 'manage_policyholders.html')

def manage_policies(request):
    return render(request, 'manage_policies.html')

def insured_persons(request):
    return render(request, 'insured_persons.html')

def manage_beneficiaries(request):
    return render(request, 'manage_beneficiaries.html')

def manage_claims(request):
    return render(request, 'manage_claims.html')

def manage_fraudprevention(request):
    return render(request, 'manage_fraudprevention.html')

def manage_airiskassessments(request):
    return render(request, 'manage_airiskassessments.html')

def manage_verifications(request):
    return render(request, 'manage_verifications.html')

def manage_lawenforcement(request):
    return render(request, 'manage_lawenforcement.html')

def manage_homeaffairs(request):
    return render(request, 'manage_homeaffairs.html')

def get_policy_details(request):
    policy_id = request.GET.get('id')
    try:
        policy = PolicyType.objects.get(id=policy_id)
        return JsonResponse({
            'premium': str(policy.premiumAmount),
            'start': policy.startDate.strftime('%Y-%m-%d'),
            'end': policy.endDate.strftime('%Y-%m-%d')
        })
    except PolicyType.DoesNotExist:
        return JsonResponse({}, status=404)