# claim/views.py
from django.shortcuts import render
from .models import Claim
from .forms import ClaimForm

def claim(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            form.save()
            form = ClaimForm()  # Reset form after successful submission
    else:
        form = ClaimForm()
    
    claims = Claim.objects.all().order_by('-dateFiled')
    return render(request, 'claim.html', {'form': form, 'claims': claims})
