# storefront/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('claim_dashboard')),  # Redirect to claim_dashboard
    path('admin/', admin.site.urls),
    path('claim/', include('claim.urls')),  # Include all claim-related URLs
]
