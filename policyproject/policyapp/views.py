from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PolicyHolder
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')

#1st login view
#def login(request):
    #if request.method == "POST":
        #email = request.POST.get('username') # this matches your form
        #password = request.POST.get('password')

        #user = authenticate(request, username=email, password=password)

        #if user is not None:
            #auth_login(request, user)
            #return redirect('dashboard')
        #else:
            #messages.error(request, "Wrong credentials.")
            #return render(request, 'login.html')

    #return render(request, 'login.html')

#2nd login view
#def login(request):
    #if request.method == "POST":
        #email = request.POST.get('username') # this matches your form
        #password = request.POST.get('password')

        #user = User.objects.get(username=email, password=password)

        #if user is not None:
            #auth_login(request, user)
            #return redirect('dashboard')
        #else:
            #messages.error(request, "Wrong credentials.")
            #return render(request, 'login.html')

    #return render(request, 'login.html')

#3rd login view
#def login(request):
    #if request.method == "POST":
        #email = request.POST.get('username') # this matches your form
        #password = request.POST.get('password')
    
        #try:
            #holder = PolicyHolder.objects.get(email=PolicyHolder.user.get_object(email), password=PolicyHolder.user.get_object(password))
            #eturn render(request, 'dashboard.html', {'holder': holder})
        #except PolicyHolder.DoesNotExist:
            #return render(request, 'login.html', {'error': 'Invalid Policy Holder credentials'})

    #return render(request, 'login.html')

#4th login view
def login(request):
    if request.method == "POST":
        email = request.POST.get('username')  # email in this case
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Wrong credentials.")
            return render(request, 'login.html')

    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        id_number = request.POST.get('id_number')
        name = request.POST.get('name')
        email = request.POST.get('email').strip().lower()
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            messages.error(request, "Passwords don’t match.")
            return render(request, 'register.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, "That email is already in use.")
            return render(request, 'register.html')

        if PolicyHolder.objects.filter(id_number=id_number).exists():
            messages.error(request, "This ID Number is already linked to a user.")
            return render(request, 'register.html')

        # Create the user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # Link to policyholder
        PolicyHolder.objects.create(
            user=user,
            id_number=id_number,
            name=name,
            phone_number=contact,
            email=email,
            address=address
        )

        messages.success(request, "You're registered successfully. You can log in.")
        return redirect('login')

    return render(request, 'register.html')

@login_required
def logout(request):
    return render(request, 'landing_page.html')

@login_required
def dashboard(request):
    policyholder = None
    if request.user.is_authenticated:
        try:
            policyholder = PolicyHolder.objects.get(user=request.user)
        except PolicyHolder.DoesNotExist:
            policyholder = None
    
    context = {
        'policyholder': policyholder,
        # other context variables
    }
    return render(request, 'dashboard.html', context)


#@login_required
#def dashboard(request):
    E#return render(request, 'dashboard.html')

#def add_policy(request):
 #   if request.method == "POST":
  #      id_number = request.POST.get('id_number')
   #     name = request.POST.get('name')
    #    address = request.POST.get('address')
     #   contact = request.POST.get('phone_number')
      #  email = request.POST.get('email')
       # password = request.POST.get('password')  # Consider hashing in real usage

        #PolicyHolder.objects.create(
         #   id_number=id_number,
          #  name=name,
           # address=address,
            #contact=contact,
            #email=email,
            #password=password
        #)
        #return redirect('dashboard')

    #return render(request, 'add-policy.html')
def add_policy(request):
    return render(request, 'add-policy.html')

def policy_status(request):
    return render(request, 'policy-status.html')

def manage_beneficiaries(request):
    return render(request, 'manage-beneficiaries.html')

def file_claim(request):
    return render(request, 'file-claim.html')

def claim_status(request):
    return render(request, 'claim-tatus.html')

def risk_report(request):
    return render(request, 'risk_report.html')

def notifications(request):
    return render(request, 'notifications.html')

def test_email(request):
    try:
        send_mail(
            'Test Subject',
            'Hello Dalphy, it works 😘 Now go rule that backend like a queen. 💅',
            settings.DEFAULT_FROM_EMAIL,  # pull from settings.py
            ['dalphy040608@gmail.com'],   # your target inbox
            fail_silently=False,
        )
        return HttpResponse("Email sent successfully, my queen 👑.")
    except Exception as e:
        return HttpResponse(f"Failed to send email 😢: {e}")