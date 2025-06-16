
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_management_view,name='user_management'),  # Optional: default route to login
    path('suspend-user/<int:user_id>/', views.suspend_user_view, name='suspend_user'),
]

