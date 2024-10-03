from django.test import TestCase
from profiles.models import Profile
from django.contrib.auth.models import User
from datetime import date


class ProfileTestCase(TestCase):
    def setUp(self):
        """Create a test profile and user"""
        user = User.objects.create_user(
            username='john_doe',
            email="john.doe@test.com",
            password="Test1234!"
        )
        Profile.objects.create(
            user=user,
            birth_date="1990-01-01",
            gender="Male",
            profile_picture="profile_pictures/default.jpg",
            phone_number="1234567890",
            bio="I am a test user"
        )

    def test_profile_data(self):
        """Test profile data"""
        profile = Profile.objects.get(user__email="john.doe@test.com")
        self.assertEqual(profile.user.first_name, '')
        self.assertEqual(profile.user.last_name, '')
        self.assertTrue(profile.user.check_password('Test1234!'))
        self.assertEqual(profile.birth_date, date(1990, 1, 1))
        self.assertEqual(profile.gender, 'Male')
        self.assertEqual(
            profile.profile_picture, 'profile_pictures/default.jpg'
        )
        self.assertEqual(profile.phone_number, '1234567890')
        self.assertEqual(profile.bio, 'I am a test user')
