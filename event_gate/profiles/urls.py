from django.urls import path
from profiles.views import (
    register_request,
    login_request,
    verify_otp_request,
    resend_otp_request,
    cancel_account_request,
    logout_request,
    protected_request,
    skip_complete_profile_request,
    complete_profile_request,
    basic_user_data_request
)

urlpatterns = [
    path('register', register_request, name='register_request'),
    path('verify-otp', verify_otp_request, name='verify_otp_request'),
    path('resend-otp', resend_otp_request, name='resend_otp_request'),
    path('cancel-account', cancel_account_request, name='cancel_account_request'),
    path('login', login_request, name='login_request'),
    path('logout', logout_request, name='logout_request'),
    path('skip-complete-profile', skip_complete_profile_request, name='skip_complete_profile_request'),
    path('complete-profile', complete_profile_request, name='complete_profile_request'),
    path('protected', protected_request, name='protected_route_request'),
    path('user/basic', basic_user_data_request, name='basic_user_data_request'),
]
