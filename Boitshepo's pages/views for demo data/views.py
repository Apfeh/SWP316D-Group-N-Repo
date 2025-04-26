from django.shortcuts import render, redirect
from datetime import datetime

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
    return render(request, 'admin_dashboard.html', context)

# ---- Home Page ----
def home(request):
    return render(request, 'home.html')

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
    return render(request, 'policy_review.html', context)

def policy_detail(request, pk):
    selected_policy = next((policy for policy in POLICIES if policy['id'] == pk), None)
    if not selected_policy:
        return redirect('policy_review')
    context = {'selected_policy': selected_policy}
    return render(request, 'policy_review.html', context)

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
    return render(request, 'claim_review.html', {'claims': claims})

# ---- Risk Reports ----
def Risk_reports(request):
    risks = [
        {"policyholder": "John Doe", "insured_persons": 2, "avg_risk_score": 85, "pattern": "Frequent Address Changes"},
        {"policyholder": "Alice Smith", "insured_persons": 1, "avg_risk_score": 70, "pattern": "Fast Claim Frequency"},
        {"policyholder": "Mark Johnson", "insured_persons": 3, "avg_risk_score": 92, "pattern": "Unrelated Beneficiaries"},
        {"policyholder": "Sophia Brown", "insured_persons": 2, "avg_risk_score": 65, "pattern": "Multiple Beneficiary Changes"},
    ]

    ai_analysis = [
        "Frequent policyholder address changes detected",
        "Multiple claims filed within a short period",
        "Insured persons unrelated to policyholder",
        "Previous fraud flags from law enforcement checks",
    ]

    timeline = [
        {"date": "Jan 2025", "event": "Policyholder address change detected"},
        {"date": "Feb 2025", "event": "Two claims filed within 1 month"},
        {"date": "Mar 2025", "event": "Investigation flagged by law enforcement database"},
        {"date": "Apr 2025", "event": "Beneficiary relationship mismatch detected"},
    ]

    context = {
        "risks": risks,
        "ai_analysis": ai_analysis,
        "timeline": timeline,
    }
    
    return render(request, "Risk_reports.html", context)

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
    return render(request, 'fraud_alerts.html', {'alerts': alerts})

# ---- User Management ----
def user_management(request):
    return render(request, 'user_management.html')
