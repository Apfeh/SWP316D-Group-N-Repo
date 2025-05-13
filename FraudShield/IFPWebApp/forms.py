# IFPWebApp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PolicyHolder

class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100, required=True)
    idno = forms.CharField(max_length=50, required=True, label='National ID Number')
    phoneNumber = forms.CharField(max_length=15, required=False, label='Phone Number')
    address = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'name', 'idno', 'phoneNumber', 'address']

    def clean_idno(self):
        idno = self.cleaned_data.get('idno')
        if PolicyHolder.objects.filter(idno=idno).exists():
            raise forms.ValidationError('This ID number is already in use.')
        return idno

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            PolicyHolder.objects.create(
                idno=self.cleaned_data['idno'],
                name=self.cleaned_data['name'],
                email=self.cleaned_data['email'],
                phoneNumber=self.cleaned_data['phoneNumber'],
                address=self.cleaned_data['address']
            )
        return user