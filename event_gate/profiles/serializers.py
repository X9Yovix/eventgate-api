from rest_framework import serializers
from profiles.services import register_service, complete_profile_service
from django.contrib.auth.models import User
from profiles.models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password'
        ]

    def create(self, validated_data):
        return register_service(validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CancelAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CompleteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['birth_date', 'gender', 'phone_number', 'bio', 'profile_picture']

    def save(self):
        user = self.context['user']
        profile = user.profile
        return self.update(profile, self.validated_data)

    def update(self, instance, validated_data):
        return complete_profile_service(instance, validated_data)
