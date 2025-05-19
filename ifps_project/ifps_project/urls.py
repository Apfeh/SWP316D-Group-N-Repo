
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.login_view),  # Optional: default route to login
    path('logout/', views.logout_view, name='logout'),
]

