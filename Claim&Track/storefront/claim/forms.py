# claim/forms.py
from django import forms
from .models import Claim

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['policyId', 'beneficiaryId', 'policyHolderId', 'claimAmount']
        widgets = {
            'claimAmount': forms.NumberInput(attrs={'step': '0.01'}),
        }
