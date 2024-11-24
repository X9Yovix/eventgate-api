from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from events.models import Event, Tag
from register.models import Interested
from rest_framework_simplejwt.tokens import RefreshToken


class InterestedInEventFunctionalTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(username='user1', email='user1@user1.com', password='user1')
        self.user2 = User.objects.create_user(username='user2', email='user2@user2.com', password='user2')

        self.tag = Tag.objects.create(name="Technology")
        self.event = Event.objects.create(
            user=self.user1,
            event_name="Event 1",
            location="12.123,13.123",
            day="2024-11-22",
            start_time="10:00:00",
            end_time="12:00:00"
        )
        self.event.tags.add(self.tag)

    def authenticate_user(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_interested_in_event(self):
        self.authenticate_user(self.user2)
        response = self.client.post(f'/api/register/interested?event_id={self.event.id}')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], "Interest in event shown successfully")
        self.assertTrue(Interested.objects.filter(user=self.user2, event=self.event).exists())

    def test_interested_in_event_not_found(self):
        self.authenticate_user(self.user2)
        response = self.client.post('/api/register/interested?event_id=999999999999')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Event not found", response.data['error'])

    def test_already_interested_in_event(self):
        Interested.objects.create(user=self.user2, event=self.event)
        self.authenticate_user(self.user2)
        response = self.client.post(f'/api/register/interested?event_id={self.event.id}')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Already interested in this event', response.data['error'])

    def test_interested_in_own_event(self):
        self.authenticate_user(self.user1)
        response = self.client.post(f'/api/register/interested?event_id={self.event.id}')
        self.assertEqual(response.status_code, 400)
        self.assertIn("You can't show interest in your own event", response.data['error'])


class RemoveInterestFunctionalTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(username='user1', email='user1@user1.com', password='user1')
        self.user2 = User.objects.create_user(username='user2', email='user2@user2.com', password='user2')

        self.tag = Tag.objects.create(name="Technology")
        self.event = Event.objects.create(
            user=self.user1,
            event_name="Event 1",
            location="12.123,13.123",
            day="2024-11-22",
            start_time="10:00:00",
            end_time="12:00:00"
        )
        self.event.tags.add(self.tag)

    def authenticate_user(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_remove_interest(self):
        Interested.objects.create(user=self.user2, event=self.event)
        self.authenticate_user(self.user2)
        response = self.client.delete(f'/api/register/interested/remove?event_id={self.event.id}')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Interested.objects.filter(user=self.user2, event=self.event).exists())

    def test_remove_interest_not_found(self):
        self.authenticate_user(self.user2)
        response = self.client.delete(f'/api/register/interested/remove?event_id={self.event.id}')
        self.assertEqual(response.status_code, 400)
        self.assertIn("You still haven't shown interest in this event", response.data['error'])

    def test_remove_interest_event_not_found(self):
        Interested.objects.create(user=self.user2, event=self.event)
        self.authenticate_user(self.user2)
        response = self.client.delete('/api/register/interested/remove?event_id=999999999999')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Event not found", response.data["error"])
