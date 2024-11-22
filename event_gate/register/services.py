from django.shortcuts import get_object_or_404
from register.models import Interested, RequestedToJoin, RequestStatus
from events.models import Event
from django.utils import timezone


def interested_in_event(user, event_id):
    event = get_object_or_404(Event, id=event_id)
    if Interested.objects.filter(user=user, event=event).exists():
        raise ValueError("Already interested in this event")
    interested = Interested.objects.create(user=user, event=event)
    return interested


def remove_interest(user, event_id):
    event = get_object_or_404(Event, id=event_id)
    interest = Interested.objects.filter(user=user, event=event).first()
    if not interest:
        raise ValueError("You still haven't shown interest in this event")
    interest.delete()
    return True


def request_to_join_event(user, event_id):
    event = get_object_or_404(Event, id=event_id)
    if RequestedToJoin.objects.filter(user=user, event=event).exists() and RequestedToJoin.objects.filter(user=user, event=event, status=RequestStatus.PENDING.name).exists():
        raise ValueError("Already requested to join this event")
    if RequestedToJoin.objects.filter(user=user, event=event).exists() and RequestedToJoin.objects.filter(user=user, event=event, status=RequestStatus.CANCELLED.name).exists():
        requested = RequestedToJoin.objects.filter(user=user, event=event).first()
        print(requested)
        requested.status = RequestStatus.PENDING.name
        requested.save()
        return True
    RequestedToJoin.objects.create(user=user, event=event, status=RequestStatus.PENDING.name)
    return True


def cancel_request(user, event_id):
    event = get_object_or_404(Event, id=event_id)
    request = RequestedToJoin.objects.filter(user=user, event=event).first()
    if not request:
        raise ValueError("Request to join event not found")
    if request.status == RequestStatus.ACCEPTED.name or request.status == RequestStatus.CANCELLED.name:
        raise ValueError("Only pending requests can be cancelled")
    request.status = RequestStatus.CANCELLED.name
    request.save()
    return True


def accept_request(auth_user, user_id, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.user != auth_user:
        raise ValueError("Only the event creator can accept requests")
    request = RequestedToJoin.objects.filter(event=event, user=user_id, status=RequestStatus.PENDING.name).first()
    if not request:
        raise ValueError("No pending requests found to accept")
    request.status = RequestStatus.ACCEPTED.name
    request.accepted_at = timezone.now()
    request.save()
    return True
