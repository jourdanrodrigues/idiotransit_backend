from django.test import TestCase

from idiotransit.core.models import Vehicle, Occurrence, User


class VehicleTestCase(TestCase):
    fixtures = ['vehicles']

    def test_delete_vehicle(self):
        vehicle = Vehicle.objects.first()

        with self.assertRaises(NotImplementedError):
            vehicle.delete()


class OccurrenceTestCase(TestCase):
    fixtures = ['vehicles', 'occurrences']

    def test_delete_occurrence(self):
        occurrence = Occurrence.objects.first()

        with self.assertRaises(NotImplementedError):
            occurrence.delete()


class UserTestCase(TestCase):
    fixtures = ['users']

    def test_user_methods(self):
        user = User.objects.first()

        with self.assertRaises(NotImplementedError):
            user.get_full_name()

        with self.assertRaises(NotImplementedError):
            user.get_short_name()
