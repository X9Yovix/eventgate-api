from django.test import TestCase
from django.contrib.auth.models import User
from events.models import Event, Tag
from register.services import request_to_join_event, cancel_request, accept_request
from register.models import RequestedToJoin, RequestStatus


class RequestToJoinEventUnitTest(TestCase):
    def setUp(self):
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

    def test_request_to_join_event(self):
        result = request_to_join_event(self.user2, self.event.id)
        self.assertTrue(result)
        self.assertEqual(RequestedToJoin.objects.count(), 1)
        request = RequestedToJoin.objects.first()
        self.assertEqual(request.user, self.user2)
        self.assertEqual(request.event, self.event)
        self.assertEqual(request.status, RequestStatus.PENDING.name)

    def test_request_to_join_event_not_found(self):
        with self.assertRaises(ValueError) as context:
            request_to_join_event(self.user2, 999999999)
        self.assertEqual(str(context.exception), "Event not found")

    def test_already_requested_to_join(self):
        RequestedToJoin.objects.create(user=self.user2, event=self.event, status=RequestStatus.PENDING.name)
        with self.assertRaises(ValueError) as context:
            request_to_join_event(self.user2, self.event.id)
        self.assertEqual(str(context.exception), "Already requested to join this event")
        self.assertEqual(RequestedToJoin.objects.count(), 1)

    def test_request_to_join_own_event(self):
        with self.assertRaises(ValueError) as context:
            request_to_join_event(self.user1, self.event.id)
        self.assertEqual(str(context.exception), "You can't request to join your own event")
        self.assertEqual(RequestedToJoin.objects.count(), 0)


class CancelRequestUnitTest(TestCase):
    def setUp(self):
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

    def test_cancel_request(self):
        RequestedToJoin.objects.create(user=self.user1, event=self.event, status=RequestStatus.PENDING.name)
        result = cancel_request(self.user1, self.event.id)
        self.assertTrue(result)
        updated_request = RequestedToJoin.objects.filter(user=self.user1, event=self.event).first()
        self.assertEqual(updated_request.status, RequestStatus.CANCELLED.name)

    def test_cancel_request_not_found(self):
        with self.assertRaises(ValueError) as context:
            cancel_request(self.user1, self.event.id)
        self.assertEqual(str(context.exception), "Request to join event not found")

    def test_cancel_request_event_not_found(self):
        with self.assertRaises(ValueError) as context:
            cancel_request(self.user2, 999999999)
        self.assertEqual(str(context.exception), "Event not found")

    def test_cancel_request_in_cancelled_state(self):
        RequestedToJoin.objects.create(user=self.user1, event=self.event, status=RequestStatus.CANCELLED.name)
        with self.assertRaises(ValueError) as context:
            cancel_request(self.user1, self.event.id)
        self.assertEqual(str(context.exception), "Only pending requests can be cancelled")

    def test_cancel_request_in_accepted_state(self):
        RequestedToJoin.objects.create(user=self.user1, event=self.event, status=RequestStatus.ACCEPTED.name)
        with self.assertRaises(ValueError) as context:
            cancel_request(self.user1, self.event.id)
        self.assertEqual(str(context.exception), "Only pending requests can be cancelled")


class AcceptRequestUnitTest(TestCase):
    def setUp(self):
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

    def test_accept_request(self):
        request = RequestedToJoin.objects.create(user=self.user2, event=self.event, status=RequestStatus.PENDING.name)
        result = accept_request(self.user1, self.user2.id, self.event.id)
        request_refreshed = RequestedToJoin.objects.get(id=request.id)
        self.assertTrue(result)
        self.assertEqual(request_refreshed.status, RequestStatus.ACCEPTED.name)

    def test_accept_request_event_not_found(self):
        with self.assertRaises(ValueError) as context:
            accept_request(self.user1, self.user2.id, 999999999)
        self.assertEqual(str(context.exception), "Event not found")

    def test_accept_request_user_not_found(self):
        with self.assertRaises(ValueError) as context:
            accept_request(self.user1, 999999999, self.event.id)
        self.assertEqual(str(context.exception), "User not found")

    def test_accept_request_as_non_creator(self):
        RequestedToJoin.objects.create(user=self.user2, event=self.event, status=RequestStatus.PENDING.name)
        with self.assertRaises(ValueError) as context:
            accept_request(self.user2, self.user2.id, self.event.id)
        self.assertEqual(str(context.exception), "Only the event creator can accept requests")
