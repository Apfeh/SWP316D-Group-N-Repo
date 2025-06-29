from django.urls import path
from IFPWebApp import views
from .views import UpdateInsuredStatus
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Main Dashboard
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact,name='contact'),
    path('terms/', views.terms,name='terms'),
    path('privacy/', views.privacy,name='privacy'),

    # Admin Pages
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('claim-review/', views.claim_review, name='claim_review'),
    path('fraud-alerts/', views.fraud_alerts, name='fraud_alerts'),
    path('policy-review/', views.policy_review, name='policy_review'),
    path('risk-reports/', views.risk_reports, name='Risk_reports'),
    path('user-management', views.user_management_view,name='user_management'),  # Optional: default route to login
    path('suspend-user/<int:user_id>/', views.suspend_user_view, name='suspend_user'),

    path('user/<int:user_id>/toggle/', views.toggle_user_status, name='toggle_user_status'),
    path('user/<int:user_id>/reset-password/', views.reset_password_view, name='reset_password'),
    path('policyholder/<str:id>/details/', views.policyholder_details_admin, name='policyholder_details_admin'),
    path('beneficiary/<int:id>/details/', views.beneficiary_details, name='beneficiary_details'),
    path('admin/<int:id>/details/', views.admin_details, name='admin_details'),
    path('insuredperson/<int:id>/simulate-death/', views.simulate_death, name='simulate_death'),
    path('insuredperson/<int:id>/details/', views.insuredperson_details, name='insuredperson_details'),
    path('user-management/', views.user_management_view, name='user_management'),

    # Dalphy's Beneficiary Pages
    #path('add-beneficiary/', views.add_beneficiary, name='add_beneficiary'),
    path('beneficiary-dashboard/', views.beneficiary_dashboard, name='beneficiary_dashboard'),
    #path('beneficiary-list/', views.beneficiary_list, name='beneficiary_list'),
    #path('beneficiary-verification/', views.beneficiary_verification, name='beneficiary_verification'),
    path('claim-status/', views.claim_status, name='claim_status'),
    #path('edit-beneficiary/', views.edit_beneficiary, name='edit_beneficiary'),
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
   
  


    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-policy/', views.add_policy, name='add_policy'),
    path('policy-status/', views.policy_status, name='policy_status'),
    path('manage-beneficiaries/', views.manage_beneficiaries, name='manage_beneficiaries'),
    path('file-claim/', views.file_claim, name='file_claim'),
    path('claim-status/', views.claim_status, name='claim_status'),
   # path('notifications/', views.notifications, name='notifications'),
  
    #Letho Fraud Detection
    path('fraud-check/<int:policyholder_id>/', views.run_manual_fraud_check, name='run_manual_fraud_check'),
    path('get-citizen/', views.get_citizen, name='get_citizen'),
    path('approve-insured/<uuid:token>/', views.approve_insured_person, name='approve_insured'),
    path('approval-success/', views.approval_success, name='approval_success'),
  #claim review
      path('claims/', views.claim_review, name='claim_review'),
      path('update-claim-status/<int:claim_id>/', views.update_claim_status, name='update_claim_status'),
    #Policy review
    path('policy_review/', views.policy_review, name='policy_review'),
    #path('policy/<int:pk>/', views.policy_detail, name='policy_detail'),
    #path('policy/<int:pk>/approve/', views.approve_policy, name='approve_policy'),
    #path('policy/<int:pk>/reject/', views.reject_policy, name='reject_policy'),
    path('update-policy-status/<int:policy_id>/', views.update_policy_status, name='update_policy_status'),

     path('policyholder/<str:id_number>/details/', views.policyholder_details, name='policyholder_details'),
    path('policyholder/<str:id_number>/insured-list/', views.insured_persons_list, name='insured_persons_list'),  # AJAX for modal
    path('insured/<int:insured_id>/details/', views.insured_person_detail, name='insured_person_detail'),
    path('policyholder/<str:id_number>/patterns/', views.suspicious_patterns, name='suspicious_patterns'),
    path('policyholder/<str:id_number>/policies/', views.policyholder_policies, name='policyholder_policies'),
    path('policyholder/<str:id_number>/beneficiaries/', views.policyholder_beneficiaries, name='policyholder_beneficiaries'),
    path('policyholder/<str:id_number>/insured/', views.policyholder_insured, name='policyholder_insured'),  # Page view
    path('policyholder/<str:id_number>/claims/', views.policyholder_claims, name='policyholder_claims'),
  
    path('insured/<int:pk>/update-status/', UpdateInsuredStatus.as_view(), name='update-insured-status'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

     path('register-face/',views.register_face, name='register_face'),
    path('verify-face/', views.verify_face, name='verify_face'),
     path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('verify-face-approval/', views.verify_face_approval, name='verify_face_approval'),


    path('admin-profile/',views.profile, name='ad_profile'),
    path('admin-notifications/',views.AdminNotis, name='ad_notifications'),


   
    path('beneficiaryLogin/', views.login_request, name='beneficiary_login'),

    path('beneficiary/login/', views.beneficiary_login, name='beneficiaryLogin'),
    path('enter-otp/', views.verify_otps, name='enter_otp'),
    path('beneficiary-dashboard/', views.beneficiary_dashboard, name='beneficiary_dashboard'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('claim-form/', views.claim_form, name='claim_form'),
    path('claim-details/', views.claim_details, name='claim_details'),
    path('support-panel/', views.support_panel, name='support_panel'),
    path('appeals-history/', views.appeals_history, name='appeals_history'),
    path('file-claim/', views.file_claim_beneficiary, name='file_claim_beneficiary'),
    path('notifications/', views.notifications_view, name='notifications'),
      path('mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
      path('get-citizen/', views.get_citizen_details, name='get_citizen_details'),
       path('get-citizen/', views.get_citizen_details, name='get_citizen_details'),
   path('delete-beneficiary/<str:beneficiary_id>/', 
     views.delete_beneficiary, 
     name='delete_beneficiary'),
    path('validate-citizen/<str:id_number>/', views.validate_citizen, name='validate_citizen'),
    path('check-duplicate-beneficiary/<str:id_number>/', views.check_duplicate_beneficiary, name='check_duplicate_beneficiary'),
    path('verify-face-beneficiary/', views.verify_face_beneficiary, name='verify_face_beneficiary'),
]
handler403 = 'IFPWebApp.views.custom_403'
handler404 = 'IFPWebApp.views.custom_404'
handler500 = 'IFPWebApp.views.custom_500'
