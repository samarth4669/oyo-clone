import uuid
from django.core.mail import send_mail
from django.conf import settings
from .models import Hotel
from django.utils.text import slugify
def generaterandomtoken():
    return str(uuid.uuid4())


def sendemailtoken(email,token):
    subject="Verify Your Email Address"
    message=f"Hi Verify Your email account by clicking this link  http://127.0.0.1:8000/accounts/verify-account/{token}"
    send_mail(
      subject,
      message,
      settings.EMAIL_HOST_USER,
      [email],
      fail_silently=False
    )
    

def sendemailotp(email,otp):
    subject="Otp For Account Login"
    message=f"Hi use this otp to login into Your Account {otp}"
    send_mail(
      subject,
      message,
      settings.EMAIL_HOST_USER,
      [email],
      fail_silently=False
    )
    


def generateslug(hotel_name):
  slug = f"{slugify(hotel_name)}-" + str(uuid.uuid4()).split('-')[0]
  if Hotel.objects.filter(hotel_slug = slug).exists():
        return generateSlug(hotel_name)
  return slug
