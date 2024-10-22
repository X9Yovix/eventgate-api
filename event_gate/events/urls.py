from django.urls import path
from events.views import create_event_request, get_all_tags_request

urlpatterns = [
    path('add', create_event_request, name='create_event_request'),
    path('tags', get_all_tags_request, name='get_all_tags_request'),
]
