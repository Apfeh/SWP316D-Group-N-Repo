'''
from .email_utils import send_otp_email
import time
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

logger = logging.getLogger(__name__)

def generate_otp():
    """Generate a 6-digit OTP"""
    import random
    return str(random.randint(100000, 999999))

def otp(request):
    """OTP input and generation page"""
    if request.method == 'POST':
        return verify_otp(request)
        
    try:
        # Clear any existing OTP session if it's expired
        if 'otp_data' in request.session:
            otp_data = request.session['otp_data']
            if time.time() - otp_data['created_at'] > 180:  # 3 minutes
                del request.session['otp_data']

        # Generate new OTP if none exists
        if 'otp_data' not in request.session:
            otp_code = generate_otp()
            email_sent = send_otp_email(otp_code, request.user.email if request.user.is_authenticated else 'kutylaalfredo@gmail.com')
            
            if not email_sent:
                messages.error(request, "Failed to send OTP email. Please try again.")
                return redirect('some_error_page')  # Replace with your error page

            request.session['otp_data'] = {
                'otp': otp_code,
                'created_at': time.time(),
                'attempts': 0,
                'resend_count': 0,
                'email_sent': email_sent,
                'last_email': time.time()
            }
            request.session.modified = True

        context = {
            'otp_display': request.session['otp_data']['otp'] if settings.DEBUG else None,
            'max_time': 180,
            'max_resend': 2,
            'total_timeout': 900
        }

        return render(request, "Beneficiary Templates/otp.html", context)

    except Exception as e:
        logger.error(f"OTP View Error: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while processing your request.")
        return redirect('some_error_page')  # Replace with your error page

def verify_otp(request):
    """OTP submission handler"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid method'})

    try:
        otp_data = request.session.get('otp_data')
        if not otp_data:
            return JsonResponse({'success': False, 'message': 'Session expired', 'is_expired': True})

        user_otp = request.POST.get('otp', '').strip()
        current_time = time.time()

        # Check if OTP is expired
        if current_time - otp_data['created_at'] > 180:
            del request.session['otp_data']
            return JsonResponse({'success': False, 'message': 'OTP expired', 'is_expired': True})

        # Check attempt limit
        if otp_data['attempts'] >= 3:
            return JsonResponse({'success': False, 'message': 'Too many attempts', 'is_locked': True})

        # Verify OTP
        if user_otp == otp_data['otp']:
            del request.session['otp_data']
            return JsonResponse({
                'success': True, 
                'redirect_url': reverse('beneficiary_verification')
            })

        # Increment failed attempts
        otp_data['attempts'] += 1
        request.session['otp_data'] = otp_data
        request.session.modified = True

        return JsonResponse({
            'success': False,
            'message': f"Invalid OTP. {3 - otp_data['attempts']} attempts left",
            'remaining_attempts': 3 - otp_data['attempts']
        })

    except Exception as e:
        logger.error(f"Verify OTP Error: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'message': 'Verification error'})

def resend_otp(request):
    """Resend OTP email"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid method'})

    try:
        otp_data = request.session.get('otp_data')
        current_time = time.time()

        if not otp_data:
            return JsonResponse({'success': False, 'message': 'Session expired', 'is_expired': True})

        # Check cooldown period (30 seconds)
        if current_time - otp_data.get('last_email', 0) < 30:
            return JsonResponse({
                'success': False, 
                'message': 'Please wait 30 seconds before requesting a new OTP',
                'on_cooldown': True
            })

        # Check max resend attempts
        if otp_data.get('resend_count', 0) >= 2:
            return JsonResponse({
                'success': False, 
                'message': 'Maximum OTP resend attempts reached',
                'is_locked': True
            })

        # Generate new OTP
        new_otp = generate_otp()
        email_sent = send_otp_email(new_otp, request.user.email if request.user.is_authenticated else 'kutylaalfredo@gmail.com')

        if not email_sent:
            return JsonResponse({
                'success': False,
                'message': 'Failed to send OTP. Please try again later.'
            })

        # Update session data
        otp_data.update({
            'otp': new_otp,
            'created_at': current_time,
            'attempts': 0,
            'resend_count': otp_data.get('resend_count', 0) + 1,
            'email_sent': True,
            'last_email': current_time
        })

        request.session['otp_data'] = otp_data
        request.session.modified = True

        return JsonResponse({
            'success': True,
            'message': 'New OTP has been sent to your email',
            'resend_count': 2 - otp_data['resend_count']
        })

    except Exception as e:
        logger.error(f"Resend OTP Error: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'message': 'Error resending OTP'})

def email_test(request):
    """Test email setup"""
    try:
        context = {'otp_code': '123456', 'valid_minutes': 5}
        success = send_otp_email(
            otp_code='123456',
            recipient='kutylaalfredo@gmail.com'
        )
        return HttpResponse("Email sent successfully." if success else "Email sending failed.")
    except Exception as e:
        logger.error(f"Email Test Error: {str(e)}", exc_info=True)
        return HttpResponse(f"Error: {str(e)}")

'''
'''
    path('', views.otp, name='otp'),  # Handles both GET and POST
    path('verify/', views.verify_otp, name='verify_otp'),
    path('resend/', views.resend_otp, name='resend_otp'),
    path('test-email/', views.email_test, name='email_test'),
    '''