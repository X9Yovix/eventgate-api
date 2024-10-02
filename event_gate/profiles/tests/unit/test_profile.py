from django.test import TestCase
from profiles.models import Profile
from datetime import date


class ProfileTestCase(TestCase):
    def setUp(self):
        """Create a test profile"""
        Profile.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@test.com",
            password="Test1234!",
            birth_date="1990-01-01",
            gender="Male",
            profile_picture="profile_pictures/default.jpg",
            phone_number="1234567890",
            bio="I am a test user"
        )

    def test_profile_data(self):
        """Test profile data"""
        profile = Profile.objects.get(email="john.doe@test.com")
        self.assertEqual(profile.first_name, 'John')
        self.assertEqual(profile.last_name, 'Doe')
        self.assertEqual(profile.password, 'Test1234!')
        self.assertEqual(profile.birth_date, date(1990, 1, 1))
        self.assertEqual(profile.gender, 'Male')
        self.assertEqual(profile.profile_picture, 'profile_pictures/default.jpg')
        self.assertEqual(profile.phone_number, '1234567890')
        self.assertEqual(profile.bio, 'I am a test user')
