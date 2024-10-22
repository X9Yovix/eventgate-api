from django.db import models
from event_gate.models import TimeStampedModel
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Event(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    event_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"{self.event_name} - {self.user.username}"


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.event.event_name}"
