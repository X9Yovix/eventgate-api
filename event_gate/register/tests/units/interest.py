from django.test import TestCase
from django.contrib.auth.models import User
from events.models import Event, Tag
from register.services import interested_in_event, remove_interest
from register.models import Interested


class InterestedInEventUnitTest(TestCase):
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

    def test_interested_in_event(self):
        interest = interested_in_event(self.user2, self.event.id)
        self.assertEqual(interest.user, self.user2)
        self.assertEqual(interest.event, self.event)
        self.assertTrue(Interested.objects.filter(user=self.user2, event=self.event).exists())

    def test_interested_in_event_not_found(self):
        with self.assertRaises(ValueError) as context:
            interested_in_event(self.user2, 999999999)

        self.assertEqual(str(context.exception), "Event not found")
        self.assertEqual(Interested.objects.count(), 0)

    def test_already_interested_in_event(self):
        Interested.objects.create(user=self.user2, event=self.event)
        with self.assertRaises(ValueError) as context:
            interested_in_event(self.user2, self.event.id)

        self.assertEqual(str(context.exception), "Already interested in this event")
        self.assertEqual(Interested.objects.count(), 1)

    def test_interested_in_own_event(self):
        with self.assertRaises(ValueError) as context:
            interested_in_event(self.user1, self.event.id)

        self.assertEqual(str(context.exception), "You can't show interest in your own event")
        self.assertEqual(Interested.objects.count(), 0)


class RemoveInterestUnitTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@user1.com', password='user1')

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

    def test_remove_interest(self):
        Interested.objects.create(user=self.user1, event=self.event)
        result = remove_interest(self.user1, self.event.id)
        self.assertTrue(result)
        self.assertEqual(Interested.objects.count(), 0)

    def test_remove_interest_not_found(self):
        with self.assertRaises(ValueError) as context:
            remove_interest(self.user1, self.event.id)
        self.assertEqual(str(context.exception), "You still haven't shown interest in this event")

    def test_remove_interest_event_not_found(self):
        with self.assertRaises(ValueError) as context:
            remove_interest(self.user1, 999999999)

        self.assertEqual(str(context.exception), "Event not found")
