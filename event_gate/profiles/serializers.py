from rest_framework import serializers
from profiles.models import Profile
from django.contrib.auth.hashers import make_password

class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'password', 'birth_date', 'gender', 'profile_picture', 'phone_number', 'bio']

    def create(self, validated_data):
        profile = Profile.objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            password = make_password(validated_data['password']),
            birth_date = validated_data['birth_date'],
            gender = validated_data['gender'],
            profile_picture = validated_data.get('profile_picture', None),
            phone_number = validated_data.get('phone_number', None),
            bio = validated_data.get('bio', None)
        )
        return profile
