"""
URL configuration for policyholder_project project.

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
from policyholders import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('policyholder_project.urls')),
]

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Dashboard as the default
    path('list/', views.list_policyholders, name='list_policyholders'),
    path('add/', views.add_policyholder, name='add_policyholder'),
    path('update/<str:id>/', views.update_policyholder, name='update_policyholder'),
]

