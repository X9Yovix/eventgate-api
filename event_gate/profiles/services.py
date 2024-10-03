from profiles.models import Profile
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
import uuid
from datetime import timedelta
from django.utils import timezone


def register_service(validated_data):
    try:
        user = User.objects.create_user(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
        )
        profile = Profile.objects.create(user=user)
        generate_otp(profile)
        send_mail(
            'Your Verification Code',
            f'Your OTP code is {profile.otp_code}. It is valid for 10 minutes.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return user

    except Exception as e:
        raise ValueError(f"Error creating user or profile: {str(e)}")


def login_service(validated_data):
    username = validated_data.get('username')
    password = validated_data.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError("User with this username does not exist")

    if not user.check_password(password):
        raise ValueError("Incorrect password")

    profile = Profile.objects.get(user=user)
    if not profile.is_verified:
        raise ValueError("Email is not verified")

    return user


def verify_opt_service(validated_data):
    otp_code = validated_data.get('otp_code')
    email = validated_data.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise ValueError("User with this email does not exist")

    profile = user.profile

    if profile.is_verified:
        raise ValueError("Email is already verified")

    if profile.otp_code == otp_code and timezone.now() < profile.otp_expiration:
        profile.is_verified = True
        profile.otp_code = None
        profile.save()
        return True

    raise ValueError("Invalid OTP or OTP has expired")


def resend_otp_service(validated_data):
    email = validated_data.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise ValueError("User with this email does not exist")

    profile = user.profile

    if profile.is_verified:
        raise ValueError("Email is already verified")

    generate_otp(profile)

    send_mail(
        'Your Verification Code',
        f'Your OTP code is {profile.otp_code}. It is valid for 10 minutes.',
        settings.DEFAULT_FROM_EMAIL,
        [profile.user.email],
        fail_silently=False,
    )


def generate_otp(profile):
    profile.otp_code = str(uuid.uuid4().int)[:6]
    profile.otp_expiration = timezone.now() + timedelta(minutes=10)
    profile.save()
