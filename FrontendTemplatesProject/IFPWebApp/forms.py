from django import forms
from .models import Beneficiary
from .models import Claim

class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = ['beneficiaryId','name', 'contactNumber', 'relationshipToInsured']

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['policyId', 'beneficiaryId', 'policyHolderId', 'claimAmount']
        widgets = {
            'claimAmount': forms.NumberInput(attrs={'step': '0.01'}),
        }