from django.urls import path
from . import views

urlpatterns = [
    # Main Dashboard
    path('', views.fraud_alerts, name='fraud_alerts'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),

    # Boitshepo's Admin Pages
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('claim-review/', views.claim_review, name='claim_review'),
    path('fraud-alerts/', views.fraud_alerts, name='fraud_alerts'),
    path('policy-review/', views.policy_review, name='policy_review'),
    path('risk-reports/', views.risk_reports, name='Risk_reports'),
    path('user-management/', views.user_management, name='user_management'),

    # Dalphy's Beneficiary Pages
    path('add-beneficiary/', views.add_beneficiary, name='add_beneficiary'),
    path('beneficiary-dashboard/', views.beneficiary_dashboard, name='beneficiary_dashboard'),
    path('beneficiary-list/', views.beneficiary_list, name='beneficiary_list'),
    path('beneficiary-verification/', views.beneficiary_verification, name='beneficiary_verification'),
    path('claim-status/', views.claim_status, name='claim_status'),
    path('edit-beneficiary/', views.edit_beneficiary, name='edit_beneficiary'),
    path('file-claim/', views.file_claim, name='file_claim'),

    # Insured Person Pages
    path('add-insured-person/', views.add_insured_person, name='add_insured_person'),
    path('consent-verification/', views.consent_verification, name='consent_verification'),
    path('insured-dashboard/', views.insured_dashboard, name='insured_dashboard'),
    path('policy-details/', views.policy_details, name='policy_details'),

    # Nyiko's Law Enforcement Pages
    path('law-dashboard/', views.law_dashboard, name='law_dashboard'),
    path('fraud-case-details/', views.fraud_case_details, name='fraud_case_details'),
    path('fraud-database-search/', views.fraud_database_search, name='fraud_database_search'),
    path('law-login/', views.law_login, name='law_login'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-policy/', views.add_policy, name='add_policy'),
    path('policy-status/', views.policy_status, name='policy_status'),
    path('manage-beneficiaries/', views.manage_beneficiaries, name='manage_beneficiaries'),
    path('file-claim/', views.file_claim, name='file_claim'),
    path('claim-status/', views.claim_status, name='claim_status'),
    
    #Letho Fraud Detection
    path('fraud-check/<int:policyholder_id>/', views.run_manual_fraud_check, name='run_manual_fraud_check'),
    
]
