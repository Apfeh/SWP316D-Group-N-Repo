from django.contrib import admin
from .models import Beneficiary, PolicyHolder

# Register your models here.
admin.site.register(Beneficiary)
admin.site.register(PolicyHolder)