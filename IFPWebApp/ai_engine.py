from datetime import timedelta
from django.utils import timezone
from .models import Claim, Policy, InsuredPerson, FraudPreventionTeam

def assess_policy_risk(holder):
    score = 0
    reasons = []

    if holder.beneficiary_changes > 3:
        score += 40
        reasons.append("Frequent beneficiary changes")
    elif holder.beneficiary_changes > 1:
        score += 20
        reasons.append("Moderate beneficiary changes")

    if holder.claims_last_year > 3:
        score += 30
        reasons.append("High claim frequency")
    elif holder.claims_last_year > 1:
        score += 15
        reasons.append("Moderate claim frequency")

    if holder.incomplete_documents:
        score += 20
        reasons.append("Incomplete documentation")

    open_claims = Claim.objects.filter(policyHolderId=holder, status__in=["Open", "Pending"]).count()
    if open_claims > 2:
        score += 25
        reasons.append("Multiple open claims")

    insured_count = InsuredPerson.objects.filter(holder=holder).count()
    if insured_count > 3:
        score += 10
        reasons.append("Multiple insured persons")

   

    recent_policies = Policy.objects.filter(policyHolder=holder, start_date__gte=timezone.now() - timedelta(days=365)).count()
    if recent_policies > 0:
        score += 10
        reasons.append("Recently issued policy")

    investigations = FraudPreventionTeam.objects.filter(policyid__policyHolder=holder).count()
    if investigations > 1:
        score += 20
        reasons.append("Multiple fraud investigations")

    score = min(score, 100)

    level = "High" if score >= 70 else "Medium" if score >= 40 else "Low"

    return {
        "score": score,
        "level": level,
        "explanation": reasons or ["No suspicious activity detected"]
    }
