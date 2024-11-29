from django.db import models
from event_gate.models import TimeStampedModel
from django.contrib.auth.models import User


User._meta.get_field('email')._unique = True


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firebase_uid = models.CharField(max_length=128, null=True, blank=True)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=10, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True)
    phone_number = models.CharField(max_length=15, null=True)
    bio = models.TextField(null=True)
    is_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, null=True)
    otp_expiration = models.DateTimeField(null=True)
    is_profile_complete = models.BooleanField(default=False)
    skip_is_profile_complete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.is_verified}'
