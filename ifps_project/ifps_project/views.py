from django.shortcuts import render, redirect
from .models import Admin, PolicyHolder, Beneficiary
from django.contrib.auth.models import User

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def suspend_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f"{user.get_full_name()} has been suspended.")
    return redirect('user_management')


def user_management_view(request):
    role = request.GET.get('role', 'all')
    status = request.GET.get('status', 'all')

    policyholders = []
    beneficiaries = []
    admins = []

    if role in ['policyholder', 'all']:
        policyholders = PolicyHolder.objects.select_related('user').all()

        if status != 'all':
            is_active = (status == 'active')
            policyholders = policyholders.filter(user__is_active=is_active)

    if role in ['beneficiary', 'all']:
        beneficiaries = Beneficiary.objects.all()
        # You can later add status filtering logic if Beneficiary has status fields

    if role in ['admin', 'all']:
        admins = User.objects.filter(is_staff=True)
        if status != 'all':
            is_active = (status == 'active')
            admins = admins.filter(is_active=is_active)

    return render(request, 'user_management.html', {
        'policyholders': policyholders,
        'beneficiaries': beneficiaries,
        'admins': admins,
        'selected_role': role,
        'selected_status': status,
    })