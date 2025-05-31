# IFPWebApp/fraud_detection.py

from django.apps import apps
from django.utils import timezone

def run_automatic_checks(policyHolder):
    Policy = apps.get_model('IFPWebApp', 'Policy')
    Beneficiary = apps.get_model('IFPWebApp', 'Beneficiary')
    SuspiciousActivity = apps.get_model('IFPWebApp', 'SuspiciousActivity')
    RiskAssessment = apps.get_model('IFPWebApp', 'RiskAssessment')

    score = 0
    now = timezone.now()

    # Rule 1: Too many unrelated policies in 12 months
    unrelated_policies = Policy.objects.filter(
        policyHolder=policyHolder,
        start_date__gte=now.replace(year=now.year - 1)
    ).count()
    if unrelated_policies > 2:
        SuspiciousActivity.objects.create(
            policyHolder=policyHolder,
            description="More than 2 unrelated policies in 12 months."
        )
        score += 30

    # Rule 2: Frequent beneficiary changes
    beneficiary_changes = Beneficiary.objects.filter(policy__policyHolder=policyHolder).count()
    if beneficiary_changes > 5:
        SuspiciousActivity.objects.create(
            policyHolder=policyHolder,
            description="Frequent beneficiary changes detected."
        )
        score += 20

    # Rule 3: High-value policies for young insured people (example only)
    high_risk_policies = Policy.objects.filter(
        policyHolder=policyHolder,
        amount__gte=500000
    ).count()
    if high_risk_policies >= 1:
        SuspiciousActivity.objects.create(
            policyHolder=policyHolder,
            description="High-value policy issued — flagged for manual review."
        )
        score += 25

    RiskAssessment.objects.create(
        policyHolder=policyHolder,
        risk_score=score,
        requires_manual_approval=score >= 50
    )