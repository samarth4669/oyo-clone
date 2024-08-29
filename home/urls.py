from django.urls import path
from .views import *
from accounts.views import vendor_dashboard,add_hotel
urlpatterns = [
    path("home",index,name="index"),
    path("vendor_dashboard", vendor_dashboard,name="vendor_dashboard"),
    path("vendor_dashboard/add_hotel",add_hotel,name="add_hotel"),
     path('hotel-details/<slug>/',hotel_details, name="hotel_details")

    
    
]
