from django.db import models
from enum import Enum
from event_gate.models import TimeStampedModel
from django.contrib.auth.models import User
from events.models import Event


class RequestStatus(Enum):
    ACCEPTED = 'Accepted'
    PENDING = 'Pending'
    CANCELLED = 'Cancelled'


class Interested(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='interested_events')
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='interested_users')

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} is interested in {self.event.event_name}"


class RequestedToJoin(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_to_join_events')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='requesting_users')
    status = models.CharField(
        max_length=10,
        choices=[(status.name, status.value) for status in RequestStatus],
        default=RequestStatus.PENDING.name
    )
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        status = self.get_status_display()
        return f"{self.user.username} requested to join {self.event.event_name} - {status}"
