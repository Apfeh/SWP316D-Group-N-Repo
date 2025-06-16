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
from django.db import IntegrityError
from django.core.exceptions import ValidationError

    
 
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

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email

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
        citizen = Citizen.objects.using('homeaffairs').get(idNumber=self.cleaned_data['id_number'])
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']  # Use username to sign in
        user.first_name = citizen.name
        user.last_name = citizen.surname
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

# forms.py
from django import forms
from .models import Citizen

class FaceRegistrationForm(forms.Form):
    id_number = forms.CharField(
        label='ID Number',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter ID number'
        })
    )
    face_image = forms.ImageField(
        label='Upload Face Image',
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            'class': 'form-control-file'
        })
    )
    
    def clean_id_number(self):
        id_number = self.cleaned_data['id_number']
        if not Citizen.objects.filter(idNumber=id_number).exists():
            raise forms.ValidationError("ID number not found in database")
        return id_number

# Remove id_number field from verification form
class FaceVerificationForm(forms.Form):
    face_image = forms.ImageField(
        label='Capture Face',
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            'capture': 'environment',
            'class': 'd-none',
            'id': 'faceCapture'
        })
    )
    face_image = forms.ImageField(
        label='Capture Face',
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            'capture': 'environment',
            'class': 'd-none',
            'id': 'faceCapture'
        })
    )