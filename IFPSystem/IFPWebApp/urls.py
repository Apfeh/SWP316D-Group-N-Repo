from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='insured_persons_list'),  # Correctly map root URL
    path('beneficiaries/', views.beneficiary_list, name='beneficiary_list'),
    path('beneficiaries/add/', views.beneficiary_create, name='beneficiary_create'),
    path('beneficiaries/edit/<int:id>/', views.beneficiary_update, name='beneficiary_update'),
    path('beneficiaries/delete/<int:id>/', views.beneficiary_delete, name='beneficiary_delete'),
    path('claim/', views.claim, name='claim'),
    path('delete/<int:id>/', views.delete_insured_person, name='delete_insured_person'),
    path('list/', views.list_policyholders, name='list_policyholders'),
    path('add/', views.add_policyholder, name='add_policyholder'),
    path('update/<str:id>/', views.update_policyholder, name='update_policyholder'),
    path('dashboard/', views.dashboard, name='dashboard'),
     path('manage-team/', views.manage_team, name='manage_team'), 
   


]
