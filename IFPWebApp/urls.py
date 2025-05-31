from django.urls import path
from IFPWebApp import views

urlpatterns = [
    # Main Dashboard
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),

    # Admin Pages
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('claim-review/', views.claim_review, name='claim_review'),
    path('fraud-alerts/', views.fraud_alerts, name='fraud_alerts'),
    path('policy-review/', views.policy_review, name='policy_review'),
    path('risk-reports/', views.risk_reports, name='Risk_reports'),
    path('user-management/', views.user_management, name='user_management'),

    # Dalphy's Beneficiary Pages
    path('add-beneficiary/', views.add_beneficiary, name='add_beneficiary'),
    path('beneficiary-dashboard/', views.beneficiary_dashboard, name='beneficiary_dashboard'),
    path('beneficiary-list/', views.beneficiary_list, name='beneficiary_list'),
    #path('beneficiary-verification/', views.beneficiary_verification, name='beneficiary_verification'),
    path('claim-status/', views.claim_status, name='claim_status'),
    path('edit-beneficiary/', views.edit_beneficiary, name='edit_beneficiary'),
   #path('facial-recognition/',views.face_recognition, name='facial_recognition'),
  
   # path('facial-recognition/', views.face_recognition, name='facial_recognition'),
     #path('verify-faces/', views.verify_faces, name='verify_face'),
    path('file-claim/', views.file_claim, name='file_claim'),

   # path('otp/', views.otp, name='otp'),
   # path('verify-otp/', views.verify_otp, name='verify_otp'),
   # path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('logout/', views.logout, name='logout'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
     path('send-otp1/', views.send_otp1, name='send_otp1'),
    path('verify-otp1/', views.verify_otp1, name='verify_otp1'),
    path('resend-otp1/', views.resend_otp1, name='resend_otp1'),
    path('approve/<str:token>/', views.approve_beneficiary, name='approve_beneficiary'),
    path('decline/<str:token>/', views.decline_beneficiary, name='decline_beneficiary'),
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
    path('notifications/', views.notifications, name='notifications'),
    path('delete-beneficiary/<int:beneficiary_id>/',views.delete_beneficiary, name='delete_beneficiary'),
    #Letho Fraud Detection
    path('fraud-check/<int:policyholder_id>/', views.run_manual_fraud_check, name='run_manual_fraud_check'),
    path('get-citizen/', views.get_citizen, name='get_citizen'),
  path('approve-insured/<uuid:token>/', views.approve_insured_person, name='approve_insured')
    
]
