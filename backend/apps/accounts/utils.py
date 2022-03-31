import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from project import settings


def generate_OTP_number():
    return random.randint(100000, 999999)


def send_OTP_number(user):
    email_template = render_to_string('accounts/login_success.html',
                                      {"username": user.username, "otp_number": user.otp_number})
    login = EmailMultiAlternatives(
        "Successfully Login",
        "Successfully Login",
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    login.attach_alternative(email_template, 'text/html')
    if not settings.DEBUG:
        login.send()


def two_factor_authentication_send_email(user):
    user.otp_number = generate_OTP_number()
    user.save()
    send_OTP_number(user)


