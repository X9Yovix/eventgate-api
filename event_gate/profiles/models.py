from django.db import models
from event_gate.models import TimeStampedModel


class Profile(TimeStampedModel):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(blank=False, null=False, unique=True)
    password = models.CharField(max_length=128, blank=False, null=False)
    birth_date = models.DateField(blank=False, null=False)
    gender = models.CharField(max_length=10, blank=False, null=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'First name: {self.first_name}, Last name: {self.last_name}'
