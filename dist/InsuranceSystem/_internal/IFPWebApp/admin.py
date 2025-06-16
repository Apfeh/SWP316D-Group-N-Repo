
from django.contrib import admin
from .models import Beneficiary, Case, Claim, InsuredPerson, Officer, PolicyHolder,Policy

# Register your models here.
admin.site.register(Beneficiary)
admin.site.register(PolicyHolder)
admin.site.register(Policy)
admin.site.register(InsuredPerson)
admin.site.register(Claim)
admin.site.register(Officer)
admin.site.register(Case)
