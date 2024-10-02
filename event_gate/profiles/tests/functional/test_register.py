from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from profiles.models import Profile

class RegistrationTests(TestCase):

    def test_empty_fields(self):
        """Test registration with empty fields"""
        response = self.client.post(reverse('register'), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_without_at_and_dot(self):
        """Test registration with invalid email"""
        response = self.client.post(reverse('register'), data={
            'email': 'invalid-email',
            'password': 'Test1234!',
            'first_name': 'John',
            'last_name': 'Doe'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_without_dot(self):
        """Test registration with invalid email"""
        response = self.client.post(reverse('register'), data={
            'email': 'invalid-email@com',
            'password': 'Test1234!',
            'first_name': 'John',
            'last_name': 'Doe'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password(self):
        """Test registration with invalid password"""
        response = self.client.post(reverse('register'), data={
            'email': 'john.doe@example.com',
            'password': 'short',
            'first_name': 'John',
            'last_name': 'Doe'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_same_password_as_email(self):
        """Test registration with invalid password"""
        response = self.client.post(reverse('register'), data={
            'email': 'john.doe@example.com',
            'password': 'john.doe@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_valid_registration(self):
        """Test valid registration"""
        response = self.client.post(reverse('register'), data={
            'email': 'john.doe@example.com',
            'password': 'john.doe@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'birth_date': '1990-01-01',
            'phone_number': '1234567890',
            'gender':'male',
            'bio':'I am a test user'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Profile.objects.filter(email='john.doe@example.com').exists())

