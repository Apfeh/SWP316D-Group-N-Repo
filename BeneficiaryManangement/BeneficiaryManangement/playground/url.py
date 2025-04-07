from django.urls import path
from . import views

urlpatterns = [
    path('beneficiaries/', views.beneficiary_list, name='beneficiary_list'),
    path('beneficiaries/add/', views.beneficiary_create, name='beneficiary_create'),
    path('beneficiaries/edit/<int:id>/', views.beneficiary_update, name='beneficiary_update'),
    path('beneficiaries/delete/<int:id>/', views.beneficiary_delete, name='beneficiary_delete'),
]
