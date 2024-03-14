from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

FROM_MAIL = 'studentepkncet@gmail.com'
FAIL_SILENTLY = False

def welcome_mail(request, user, email, passw):
    """Send a Welcome email to the user."""

    subject = 'Welcome to Medic India'
    message = f'Dear {user.first_name} {user.last_name},\nWelcome to the Medic India.\nYour Login Credentials:\n\nEmail: {email}\nPassword: {passw}\n\nA verification email has been sent. Please verify your account.\n\n\n\nRegards,\nDinagar K\nDeveloper.'
    recipient_list = [user.email]

    send_mail(subject, message, FROM_MAIL, recipient_list, fail_silently=FAIL_SILENTLY)

def verification_email(request, user):
    """Send a verification email to the user."""

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = request.build_absolute_uri(f"/verify/{uid}/{token}/")
    subject = 'Verify Your Account'
    message = f'Dear {user.first_name} {user.last_name},\nClick the following link to verify your account:\n {verification_url}\n\n\n\nRegards,\nDinagar K\nDeveloper.'
    recipient_list = [user.email]

    send_mail(subject, message, FROM_MAIL, recipient_list, fail_silently=FAIL_SILENTLY)
    
    