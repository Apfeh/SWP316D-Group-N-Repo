"""
URL configuration for policyproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from policyapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('policyproject.urls')),
]

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-policy/', views.add_policy, name='add_policy'),
    path('policy-status/', views.policy_status, name='policy_status'),
    path('manage-beneficiaries/', views.manage_beneficiaries, name='manage_beneficiaries'),
    path('file-claim/', views.file_claim, name='file_claim'),
    path('claim-status/', views.claim_status, name='claim_status'),
    path('risk_report/', views.risk_report, name='risk_report'),
    path('notifications/', views.notifications, name='notifications'),
    path('test-email/', views.test_email, name='test_email'),
]