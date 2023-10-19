import random
import string
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import OTP


def generate_otp(length=6):
    while True:
        characters = string.digits
        otp = "".join(random.choice(characters) for _ in range(length))
        if OTP.objects.filter(otp_code=otp).exists():
            continue
        else:
            return otp


def send_otp_email(user_id, email, otp_code):
    my_subject = "OTP Job Kit"
    context = {
        "otp_code": otp_code,
    }
    recipient_list = [email]
    html_message = render_to_string("otp.html", context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=my_subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
    )
    message.attach_alternative(html_message, "text/html")
    message.send()
    OTP.objects.create(user_id=user_id, otp_code=otp_code)
