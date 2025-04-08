
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='insured_persons_list'),
    path('delete/<int:id>/', views.delete_insured_person, name='delete_insured_person'),
]

