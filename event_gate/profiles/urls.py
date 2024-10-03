from django.urls import path
from profiles.views import (
    register_request,
    login_request,
    verify_otp_request,
    resend_otp_request,
    logout_request,
    protected_request
)

urlpatterns = [
    path('register', register_request, name='register_request'),
    path('verify-otp', verify_otp_request, name='verify_otp_request'),
    path('resend-otp', resend_otp_request, name='resend_otp_request'),
    path('login', login_request, name='login_request'),
    path('logout', logout_request, name='logout_request'),
    path('protected', protected_request, name='protected_route_request'),
]
