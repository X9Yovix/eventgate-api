from django.urls import path
from events.views import create_event_request, get_all_tags_request, get_recent_events_request, get_event_request

urlpatterns = [
    path('add', create_event_request, name='create_event_request'),
    path('tags', get_all_tags_request, name='get_all_tags_request'),
    path('recent', get_recent_events_request, name='get_recent_events_request'),
    path('', get_event_request, name='get_event_request'),
]
