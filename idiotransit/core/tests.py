from django.db import IntegrityError
from django.test import TestCase

from idiotransit.core.models import Vehicle, Occurrence, User


class VehicleTestCase(TestCase):
    fixtures = ['vehicles']

    def test_delete_vehicle(self):
        vehicle = Vehicle.objects.first()

        with self.assertRaises(NotImplementedError):
            vehicle.delete()

    def test_vehicle_creation(self):
        license_plate = 'ASD-1234'
        common_args = {'license_plate': license_plate}

        Vehicle.objects.create(**common_args)
        self.assertTrue(Vehicle.objects.filter(owner__isnull=True, **common_args).exists())

        with self.assertRaises(IntegrityError):
            # Since license plate must be unique, a second creation of the same license plate should not be allowed
            Vehicle.objects.create(**common_args)


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
