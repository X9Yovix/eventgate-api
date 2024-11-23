from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from events.models import Event, Tag
from register.models import RequestedToJoin, RequestStatus
from rest_framework_simplejwt.tokens import RefreshToken


class RequestToJoinEventFunctionalTests(APITestCase):
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

    def test_request_to_join_event(self):
        self.authenticate_user(self.user2)
        response = self.client.post(f'/api/register/request?event_id={self.event.id}')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], "Request to join event sent successfully")
        self.assertTrue(RequestedToJoin.objects.filter(user=self.user2, event=self.event).exists())

    def test_request_to_join_event_not_found(self):
        self.authenticate_user(self.user2)
        response = self.client.post('/api/register/request?event_id=999999999')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Event not found", response.data['error'])

    def test_already_requested_to_join(self):
        RequestedToJoin.objects.create(user=self.user2, event=self.event, status=RequestStatus.PENDING.name)
        self.authenticate_user(self.user2)
        response = self.client.post(f'/api/register/request?event_id={self.event.id}')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Already requested to join this event", response.data['error'])

    def test_request_to_join_own_event(self):
        self.authenticate_user(self.user1)
        response = self.client.post(f'/api/register/request?event_id={self.event.id}')
        self.assertEqual(response.status_code, 400)
        self.assertIn("You can't request to join your own event", response.data['error'])


class CancelRequestFunctionalTests(APITestCase):
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

    def test_cancel_request(self):
        RequestedToJoin.objects.create(user=self.user2, event=self.event, status=RequestStatus.PENDING.name)
        self.authenticate_user(self.user2)
        response = self.client.delete(f'/api/register/request/cancel?event_id={self.event.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Request cancelled successfully", response.data['message'])
        updated_request = RequestedToJoin.objects.get(user=self.user2, event=self.event)
        self.assertEqual(updated_request.status, RequestStatus.CANCELLED.name)

    def test_cancel_request_not_found(self):
        self.authenticate_user(self.user2)
        response = self.client.delete(f'/api/register/request/cancel?event_id={self.event.id}')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Request to join event not found", response.data['error'])

    def test_cancel_request_event_not_found(self):
        self.authenticate_user(self.user2)
        response = self.client.delete('/api/register/request/cancel?event_id=999999999')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Event not found", response.data['error'])

    def test_cancel_request_in_cancelled_state(self):
        RequestedToJoin.objects.create(user=self.user2, event=self.event, status=RequestStatus.CANCELLED.name)
        self.authenticate_user(self.user2)

        response = self.client.delete(f'/api/register/request/cancel?event_id={self.event.id}')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Only pending requests can be cancelled", response.data['error'])

    def test_cancel_request_in_accepted_state(self):
        RequestedToJoin.objects.create(user=self.user2, event=self.event, status=RequestStatus.ACCEPTED.name)
        self.authenticate_user(self.user2)

        response = self.client.delete(f'/api/register/request/cancel?event_id={self.event.id}')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Only pending requests can be cancelled", response.data['error'])


class AcceptRequestFunctionalTests(APITestCase):
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

    def test_accept_request(self):
        RequestedToJoin.objects.create(user=self.user2, event=self.event, status=RequestStatus.PENDING.name)
        self.authenticate_user(self.user1)
        response = self.client.patch(f'/api/register/request/accept?event_id={self.event.id}&user_id={self.user2.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Request accepted successfully", response.data['message'])

        updated_request = RequestedToJoin.objects.get(user=self.user2, event=self.event)
        self.assertEqual(updated_request.status, RequestStatus.ACCEPTED.name)

    def test_accept_request_event_not_found(self):
        self.authenticate_user(self.user1)
        response = self.client.patch('/api/register/request/accept?event_id=999999999&user_id=1')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Event not found", response.data['error'])

    def test_accept_request_user_not_found(self):
        self.authenticate_user(self.user1)
        response = self.client.patch(f'/api/register/request/accept?event_id={self.event.id}&user_id=999999999')
        self.assertEqual(response.status_code, 400)
        self.assertIn("User not found", response.data['error'])

    def test_accept_request_as_creator(self):
        RequestedToJoin.objects.create(user=self.user2, event=self.event, status=RequestStatus.PENDING.name)
        self.authenticate_user(self.user2)
        response = self.client.patch(f'/api/register/request/accept?event_id={self.event.id}&user_id={self.user2.id}')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Only the event creator can accept requests", response.data['error'])
