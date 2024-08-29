from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.contrib import messages
from .utils import generaterandomtoken,sendemailtoken,sendemailotp,generateslug
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.


def loginview(request):
    if(request.method=="POST"):
        email=request.POST.get('email')
        password=request.POST.get('password')

        hotel_user=Hoteluser.objects.filter(email=email)
        if( not hotel_user.exists()):
            messages.warning(request,"No Account Found")
            return redirect("/accounts/register")
        if( not hotel_user[0].is_verified):
            messages.warning(request,"Account Not Verified")
            return redirect("/accounts/login") 

        hotel_user=authenticate(username=hotel_user[0].username,password=password)
        if(hotel_user):
            messages.success(request,"Login Succesful")
            login(request,hotel_user)
            return redirect("/home") 
        
        messages.warning(request,"Login Unsuccesful")
        return redirect("/accounts/login") 

        

        
    
    return render(request,"login.html")


def registerview(request):
    if(request.method=="POST"):
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        phone_number=request.POST.get('phone_number')
        password=request.POST.get('password')

        hotel_user=Hoteluser.objects.filter(Q(phone_number=phone_number) | Q(email=email))

        if(hotel_user.exists()):
            messages.warning(request,"Account exists with Email or Phone_number")
            return redirect("/accounts/register")
        hotel_user=Hoteluser.objects.create(first_name=first_name,last_name=last_name,email=email,phone_number=phone_number,email_token=generaterandomtoken())
        hotel_user.set_password(password)
        hotel_user.save()   
        sendemailtoken(email,hotel_user.email_token)
        messages.success(request,"Verify Your Email")

        return redirect("/accounts/register") 

        
    return render(request,"register.html")


def verify_email_token(request,token):
    try:

        hotel_user=Hoteluser.objects.get(email_token=token)
        hotel_user.is_verified=True
        hotel_user.save()
        messages.success(request,"Email Verified")

        return redirect("/accounts/login") 
    except Exception as e:
        return HttpResponse("Invalid User Token")


def send_otp(request,email):
    hotel_user=Hoteluser.objects.filter(email=email)
    if(not hotel_user.exists()):
        messages.warning(request,"There is No account For given Email")
        return redirect("/accounts/login")
    
    otp=random.randint(1000,9999)
    hotel_user.update(otp=otp)
    
    sendemailotp(email,otp)
    messages.success(request,"Otp Sent To Your Mail")
    return redirect(f"/accounts/verify-otp/{email}")


def verify_otp(request,email):
    if(request.method=='POST'):
        otp=request.POST.get('otp')
        user=Hoteluser.objects.get(email=email)
        
        if(otp==user.otp):
            messages.success(request,"Login Succesful")
            login(request,user)
            return redirect("/home") 
        messages.warning(request,"Wrong Otp")
        return redirect(f"/accounts/verify-otp/{email}")

    return render(request,"verify_otp.html")


def register_vendor(request):
    if(request.method=="POST"):
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        phone_number=request.POST.get('phone_number')
        password=request.POST.get('password')
        business_name=request.POST.get('business_name')

        hotel_vendor=HotelVendor.objects.filter(Q(phone_number=phone_number) | Q(email=email))

        if(hotel_vendor.exists()):
            messages.warning(request,"Account exists with Email or Phone_number")
            return redirect("/accounts/register")
        hotel_vendor=HotelVendor.objects.create(first_name=first_name,last_name=last_name,email=email,phone_number=phone_number,email_token=generaterandomtoken(),business_name=business_name)
        hotel_vendor.set_password(password)
        hotel_vendor.save()   
        sendemailtoken(email,hotel_vendor.email_token)
        messages.success(request,"Verify Your Email")

        return redirect("/accounts/vendor-register") 

        
    return render(request,"vendor/register_vendor.html")




def login_vendor(request):
    if(request.method=="POST"):
        email=request.POST.get('email')
        password=request.POST.get('password')

        hotel_vendor=HotelVendor.objects.filter(email=email)
        if( not hotel_vendor.exists()):
            messages.warning(request,"No Account Found")
            return redirect("/accounts/vendor-register")
        if( not hotel_vendor[0].is_verified):
            messages.warning(request,"Account Not Verified")
            return redirect("/accounts/vendor-login") 

        hotel_vendor=authenticate(username=hotel_vendor[0].username,password=password)
        if(hotel_vendor):
           
            login(request,hotel_vendor)
            return redirect("/vendor_dashboard") 
        
        messages.warning(request,"Login Unsuccesful")
        return redirect("/accounts/vendor-login") 

        

        
    
    return render(request,"vendor/login_vendor.html")


@login_required(login_url='vendor-login')
def vendor_dashboard(request):
    hotels=Hotel.objects.filter(hotel_owner=request.user)
    print(hotels)
    return render(request,"vendor/vendor_dashboard.html",{'hotels':hotels})



@login_required(login_url='vendor-login')
def add_hotel(request):
    if(request.method=="POST"):
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        ameneties= request.POST.getlist('amenities')
        hotel_price= request.POST.get('hotel_price')
        hotel_offer_price= request.POST.get('hotel_offer_price')
        hotel_location= request.POST.get('hotel_location')
        hotel_slug = generateslug(hotel_name)
        hotel_vendor=HotelVendor.objects.get(id=request.user.id)
        print(ameneties)
        hotel_obj=Hotel.objects.create(
            hotel_name=hotel_name,
            hotel_description=hotel_description,
            hotel_offer_price=hotel_offer_price,
            hotel_price=hotel_price,
            hotel_slug=hotel_slug,
            hotel_owner=hotel_vendor,
            hotel_location=hotel_location

        )
        for aminity in ameneties:
            obj=Ameneties.objects.get(pk=aminity)
            hotel_obj.ameneties.add(obj)
            hotel_obj.save()


        messages.success(request,"Hotel Created")

        return redirect("/vendor_dashboard/add_hotel") 
    ameneties=Ameneties.objects.all()
    return render(request,"vendor/add_hotel.html",{'amenity':ameneties})



@login_required(login_url='vendor-login')
def upload_images(request,slug):
    hotel_obj=Hotel.objects.get(hotel_slug=slug)
    if(request.method=="POST"):
        
        image=request.FILES['image']
        HotelImages.objects.create(
            hotel=hotel_obj,
            image=image
        )
        print(image)
        return HttpResponseRedirect(request.path_info)
    return render(request,"vendor/uploadimages.html",{'images':hotel_obj.hotel_images.all()})


@login_required(login_url='vendor-login')
def delete_image(request,id):
    hotel_image=HotelImages.objects.get(id=id)
    hotel_image.delete()
    messages.success(request,"Hotel Image Deleted")
    
    return redirect('/vendor_dashboard')


# views.py
@login_required(login_url='login_vendor')
def edit_hotel(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
    
    # Check if the current user is the owner of the hotel
    if request.user.id != hotel_obj.hotel_owner.id:
        return HttpResponse("You are not authorized")

    if request.method == "POST":
        # Retrieve updated hotel details from the form
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('hotel_location')
        
        # Update hotel object with new details
        hotel_obj.hotel_name = hotel_name
        hotel_obj.hotel_description = hotel_description
        hotel_obj.hotel_price = hotel_price
        hotel_obj.hotel_offer_price = hotel_offer_price
        hotel_obj.hotel_location = hotel_location
        hotel_obj.save()
        
        messages.success(request, "Hotel Details Updated")

        return HttpResponseRedirect(request.path_info)

    # Retrieve amenities for rendering in the template
    ameneties = Ameneties.objects.all()
    
    # Render the edit_hotel.html template with hotel and amenities as context
    return render(request, 'vendor/edit_hotel.html', context={'hotel': hotel_obj, 'ameneties': ameneties})


def logout_view(request):
    logout(request)
    messages.success(request,"Logout Succesful")
    return redirect('/accounts/vendor-login')