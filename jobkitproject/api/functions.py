import random
import string
from django.core.mail import send_mail
from django.conf import settings
from .models import OTP


def generate_otp(length=6):
    characters = string.digits
    otp = "".join(random.choice(characters) for _ in range(length))
    return otp


def send_otp_email(user_id, email, otp_code):
    subject = "OTP Verification"
    message = f"Your OTP code is: {otp_code}"
    recipient_list = [email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    OTP.objects.create(user_id=user_id, otp_code=otp_code)
