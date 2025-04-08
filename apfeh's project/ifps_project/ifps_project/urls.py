
from django.urls import path
from . import views

urlpatterns = [
    
    path('manage-team/', views.manage_team, name='manage_team'),
]
