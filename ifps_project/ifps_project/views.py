from django.shortcuts import render, redirect
from .models import Admin, PolicyHolder

def login_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if role == 'admin':
            try:
                admin = Admin.objects.get(username=username, password=password)
                return render(request, 'admin_dashboard.html', {'admin': admin})
            except Admin.DoesNotExist:
                return render(request, 'login.html', {'error': 'Invalid Admin credentials'})

        elif role == 'policy_holder':
            try:
                holder = PolicyHolder.objects.get(username=username, password=password)
                return render(request, 'dashboard.html', {'holder': holder})
            except PolicyHolder.DoesNotExist:
                return render(request, 'login.html', {'error': 'Invalid Policy Holder credentials'})

    # GET request or any other case, no error passed
    return render(request, 'login.html', {'error': None})

def logout_view(request):
    # Clear the session (or any login state)
    request.session.flush()
    return redirect('login') # Redirect to login page after logout