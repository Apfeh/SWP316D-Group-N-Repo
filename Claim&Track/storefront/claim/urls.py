# claim/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.claim, name='claim_dashboard'),  # This makes claim_dashboard the default route
]
