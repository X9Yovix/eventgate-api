from django.urls import path
from register.views import (
    request_to_join_event_request,
    interested_in_event_request,
    cancel_request_request,
    accept_request_request,
    remove_interest_request,
    check_user_event_status_request
)

urlpatterns = [
    path('interested', interested_in_event_request, name='interested_in_event_request'),
    path('interested/remove', remove_interest_request, name='remove_interest_request'),

    path('request', request_to_join_event_request, name='request_to_join_event_request'),
    path('request/cancel', cancel_request_request, name='cancel_request_request'),
    path('request/accept', accept_request_request, name='accept_request_request'),

    path('event/status', check_user_event_status_request, name='check_user_event_status_request'),
]
