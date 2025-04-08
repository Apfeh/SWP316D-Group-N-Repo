# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.index, name='home') ,
    path('policyholder/manage/', views.manage_policyholders, name='manage_policyholders'),
    path('policy/manage/', views.manage_policies, name='manage_policies'),
    path('insuredperson/manage/', views.insured_persons, name='insured_persons'),
    path('beneficiary/manage/', views.manage_beneficiaries, name='manage_beneficiaries'),
    path('claim/manage/', views.manage_claims, name='manage_claims'),
    path('fraudprevention/manage/', views.manage_fraudprevention, name='manage_fraudprevention'),
    path('airiskassessment/manage/', views.manage_airiskassessments, name='manage_airiskassessments'),
    path('verification/manage/', views.manage_verifications, name='manage_verifications'),
    path('lawenforcement/manage/', views.manage_lawenforcement, name='manage_lawenforcement'),
    path('homeaffairs/manage/', views.manage_homeaffairs, name='manage_homeaffairs'),
      path('policy/get-details/', views.get_policy_details, name='get_policy_details'),
]
