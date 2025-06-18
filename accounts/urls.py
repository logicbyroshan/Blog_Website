# --- FILE: accounts/urls.py ---

from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Custom Views for User Registration and Profile
    path('signup/', views.signup_view, name='signup'),
    path('otp-verification/', views.otp_verification_view, name='otp_verification'),
    path('otp-resend/', views.resend_otp_view, name='resend_otp'), # <-- Added this line
    path('profile/', views.profile_view, name='profile'),
    
    # Django's Built-in Auth Views for Login
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),

    # Django's Built-in Password Reset Flow
    # 1. User requests a password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
        success_url=reverse_lazy('accounts:password_reset_done') # Use reverse_lazy for success URLs
    ), name='password_reset'),
    
    # 2. Page shown after the user has been sent a password reset email
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    
    # 3. The link in the email goes here, where the user enters a new password
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password_reset_confirm'),

    # 4. Page shown after the password has been successfully reset
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),

]