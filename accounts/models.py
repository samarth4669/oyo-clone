from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.


class Hoteluser(User):
    
    profile_picture=models.ImageField(upload_to="profiles")
    phone_number=models.CharField(unique=True,max_length=100)
    email_token=models.CharField(max_length=50,null=True,blank=True)
    otp=models.CharField(max_length=10,null=True,blank=True)
    is_verified=models.BooleanField(default=False)

    class Meta:
        db_table="hotel_user"


class HotelVendor(User):
    profile_picture=models.ImageField(upload_to="profiles")
    phone_number=models.CharField(unique=True,max_length=100)
    email_token=models.CharField(max_length=50,null=True,blank=True)
    otp=models.CharField(max_length=10,null=True,blank=True)
    business_name = models.CharField(max_length = 100,default="-")
    is_verified=models.BooleanField(default=False)

    class Meta:
        db_table="hotel_vendor"

class Ameneties(models.Model):
    amenetie_name=models.CharField(max_length=100)
    icon=models.ImageField(upload_to="hotels")

    def __str__(self):
        return self.amenetie_name

class Hotel(models.Model):
    hotel_name=models.CharField(max_length=100)
    hotel_description=models.TextField()
    hotel_slug=models.SlugField(max_length=100,unique=True)
    hotel_owner=models.ForeignKey(HotelVendor,  on_delete=models.CASCADE,related_name="hotels")
    ameneties=models.ManyToManyField(Ameneties)
    hotel_price=models.FloatField()
    hotel_offer_price=models.FloatField()
    hotel_location=models.TextField()
    is_active=models.BooleanField(default=True)

    


class HotelImages(models.Model):
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name="hotel_images")
    image=models.ImageField(upload_to="images")

class HotelManager(models.Model):
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name="hotel_managers")
    manager_name=models.CharField(max_length=100)
    manager_contact=models.CharField(max_length=100)
