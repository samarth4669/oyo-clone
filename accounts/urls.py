from django.urls import path
from .views import *
urlpatterns = [
    path("login/",loginview,name="loginview"),
    path("register/",registerview,name="registerview"),
    path("verify-account/<token>",verify_email_token,name="verify_email_token"),
    path("send-otp/<email>",send_otp,name="send_otp"),
    path("verify-otp/<email>",verify_otp,name="verify_otp"),
    path("vendor-register",register_vendor,name="register_vendor"),
    path("vendor-login",login_vendor,name="login_vendor"),
    path("upload_images/<slug>",upload_images,name="upload_images"),
    path("delete_image/<id>",delete_image,name="delete_image"),
    path("edit-hotel/<slug>",edit_hotel,name="edit_hotel"),
    path('logout/' ,logout_view , name="logout_view"),




]