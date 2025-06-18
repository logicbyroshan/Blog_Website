# --- FILE: accounts/views.py ---

import random
import logging
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from .forms import CustomUserCreationForm, EditProfileForm
# ... (all imports remain the same) ...
from blog_app.models import Post, Comment # <-- Import Post and Comment for counting
# It's good practice to get the logger for the current file
logger = logging.getLogger(__name__)


def send_otp_email(request, user, otp):
    """A simple helper function to send the OTP email."""
    subject = "Your Verification Code for Roshan's Writings"
    message = f"Welcome to Roshan's Writings! Your verification code is {otp}."
    
    # This is the function that actually connects to your mail server
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False, # Set to False to see errors in the console
    )


def signup_view(request):
    """
    Handles user registration with detailed step-by-step terminal messages for debugging.
    """
    # Use a clear separator in the terminal for each request
    print("\n" + "="*50)
    print("--- Starting Signup Process ---")

    if request.method == 'POST':
        print("Step 1: Received a POST request.")
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            print("Step 2: Form data is valid. Proceeding to create user.")
            
            # Save the user but keep them inactive until they verify their email
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            print(f"Step 3: Inactive user '{user.username}' created successfully in the database.")

            # Generate and store OTP in the user's session
            otp = random.randint(100000, 999999)
            request.session['otp_code'] = otp
            request.session['verification_user_id'] = user.id
            request.session['otp_expiry'] = (timezone.now() + timedelta(minutes=10)).isoformat()
            request.session['resend_cooldown_expiry'] = (timezone.now() + timedelta(seconds=60)).isoformat()
            request.session.save() # Explicitly save the session before the next step
            print(f"Step 4: OTP '{otp}' generated and saved to session for user ID {user.id}.")

            try:
                print("Step 5: Attempting to call the send_otp_email function...")
                send_otp_email(request, user, otp)
                print("Step 6: send_otp_email function completed WITHOUT raising an error.")
                
                messages.info(request, f'A verification code has been sent to {user.email}. Please check your inbox and spam folder.')
                print("Step 7: Success message added. Preparing to redirect to the OTP verification page.")
                return redirect('accounts:otp_verification')

            except Exception as e:
                # This block runs ONLY if send_otp_email fails
                print(f"---!!! CRITICAL ERROR at Step 5 !!!---")
                print(f"The send_otp_email function failed. The user was NOT redirected.")
                print(f"REASON: {e}") # This will print the exact SMTP or connection error
                logger.error(f"Failed to send OTP email for {user.username}. Error: {e}", exc_info=True)
                
                messages.error(request, 'We could not send a verification email. Please try again later.')
                user.delete() # Important: Clean up the inactive user we created
                print("Step 5b: Deleted the inactive user due to email sending failure.")
                return redirect('accounts:signup')
        
        else:
            # This block runs if the form data itself is invalid
            print("Step 2b: Form is NOT valid. It will be re-rendered with errors.")
            print("Form Errors:", form.errors.as_json())
            messages.error(request, 'Please correct the errors shown below.')

    else:
        # This block runs for a GET request (when the user first visits the page)
        print("Step 1b: Received a GET request. Displaying the empty signup form.")
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def otp_verification_view(request):
    """Verifies the OTP submitted by the user and activates the account."""
    if 'verification_user_id' not in request.session:
        messages.error(request, 'Your verification session has expired. Please sign up again.')
        return redirect('accounts:signup')

    if request.method == 'POST':
        submitted_otp = request.POST.get('otp')
        otp_code = request.session.get('otp_code')
        user_id = request.session.get('verification_user_id')

        if submitted_otp == str(otp_code):
            try:
                user = User.objects.get(id=user_id)
                user.is_active = True
                user.save()
                login(request, user)
                request.session.flush() # Clear the entire session on success
                messages.success(request, 'Your account has been verified successfully!')
                return redirect('blog_app:home')
            except User.DoesNotExist:
                messages.error(request, 'User not found. Please sign up again.')
                return redirect('accounts:signup')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    
    # Logic for the resend timer
    resend_cooldown_expiry_str = request.session.get('resend_cooldown_expiry')
    can_resend, time_left = True, 0
    if resend_cooldown_expiry_str:
        expiry_time = timezone.datetime.fromisoformat(resend_cooldown_expiry_str)
        if timezone.now() < expiry_time:
            can_resend = False
            time_left = (expiry_time - timezone.now()).seconds
    
    return render(request, 'accounts/otp_verification.html', {'can_resend': can_resend, 'time_left': time_left})


def resend_otp_view(request):
    """Generates and resends a new OTP if the cooldown period has passed."""
    user_id = request.session.get('verification_user_id')
    resend_cooldown_expiry_str = request.session.get('resend_cooldown_expiry')

    if not user_id:
        return redirect('accounts:signup')
    
    if resend_cooldown_expiry_str and timezone.now() < timezone.datetime.fromisoformat(resend_cooldown_expiry_str):
        messages.warning(request, 'Please wait before requesting another code.')
        return redirect('accounts:otp_verification')

    try:
        user = User.objects.get(id=user_id)
        otp = random.randint(100000, 999999)
        
        # Update session with new OTP and reset cooldown
        request.session['otp_code'] = otp
        request.session['otp_expiry'] = (timezone.now() + timedelta(minutes=10)).isoformat()
        request.session['resend_cooldown_expiry'] = (timezone.now() + timedelta(seconds=60)).isoformat()
        request.session.save()

        send_otp_email(request, user, otp)
        messages.success(request, 'A new verification code has been sent.')
    except Exception as e:
        logger.error(f"CRITICAL: Failed to RESEND OTP for user {user.username}. Error: {e}")
        messages.error(request, 'Failed to send a new code. Please try again later.')

    return redirect('accounts:otp_verification')



@login_required
def profile_view(request):
    """
    Displays the profile of the currently logged-in user with their activity stats.
    """
    user = request.user
    
    # Fetch real activity data from the database
    comments_written_count = Comment.objects.filter(author=user).count()
    posts_appreciated_count = user.appreciated_posts.count()
    posts_published_count = Post.objects.filter(author=user, status=Post.Status.PUBLISHED).count()

    context = {
        'user': user,
        'comments_written_count': comments_written_count,
        'posts_appreciated_count': posts_appreciated_count,
        'posts_published_count': posts_published_count,
    }
    return render(request, 'accounts/profile.html', context)

# --- ADD THIS NEW VIEW ---
@login_required
def edit_profile_view(request):
    """
    Handles updating the user's profile information.
    """
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})