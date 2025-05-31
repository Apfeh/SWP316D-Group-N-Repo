from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PolicyHolder

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PolicyHolder

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Citizen, PolicyHolder

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Citizen, PolicyHolder, Address

class CustomRegistrationForm(UserCreationForm):
    id_number = forms.CharField(
        max_length=20,
        required=True,
        help_text="Enter your government-issued ID number"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None  # Remove default help text

    def clean_id_number(self):
        id_number = self.cleaned_data['id_number']
        
        # Check Home Affairs DB
        if not Citizen.objects.using('homeaffairs').filter(idNumber=id_number).exists():
            raise forms.ValidationError("Invalid ID number - not found in national registry")
            
        # Check local PolicyHolder DB
        if PolicyHolder.objects.filter(id_number=id_number).exists():
            raise forms.ValidationError("This ID number is already registered")
            
        return id_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Use email as username
        
        if commit:
            user.save()
            
            # Get citizen data from Home Affairs
            citizen = Citizen.objects.using('homeaffairs').get(idNumber=self.cleaned_data['id_number'])
            address = Address.objects.using('homeaffairs').filter(idNumber=citizen).first()
            
            # Create PolicyHolder with data from Home Affairs
            PolicyHolder.objects.create(
                user=user,
                id_number=citizen.idNumber,
                # In your save() method:
                phone_number = address.phone_number if address and address.phone_number else '',
                name=f"{citizen.name} {citizen.surname}",
                email = user.email,
            )
            
        return user

