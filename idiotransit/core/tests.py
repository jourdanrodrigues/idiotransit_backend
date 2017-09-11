from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Count
from django.test import TestCase
from django.utils.translation import ugettext as _

from idiotransit.core.models import Vehicle, Occurrence, User, Reply, VehicleOwnershipRequest


class VehicleTestCase(TestCase):
    fixtures = ['vehicles', 'users']

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
    fixtures = ['vehicles', 'occurrences', 'users']

    def test_occurrence_creation(self):
        data = {'vehicle': Vehicle.objects.first(), 'description': 'A nice and sweet message about what happened'}
        Occurrence.objects.create(**data)
        self.assertTrue(Occurrence.objects.filter(user__isnull=True, **data).exists())

    def test_delete_occurrence(self):
        with self.assertRaises(NotImplementedError):
            Occurrence.objects.first().delete()


class UserTestCase(TestCase):
    fixtures = ['users', 'vehicles', 'occurrences', 'replies']

    def test_set_occurrences_to_null_on_delete(self):
        user = User.objects.filter(occurrences__isnull=False).first()
        occurrences_ids = list(user.occurrences.values_list('id', flat=True))  # "list" to force query execution
        user.delete()

        self.assertTrue(Occurrence.objects.filter(user__isnull=True, id__in=occurrences_ids).exists())

    def test_set_vehicles_to_null_on_delete(self):
        user = User.objects.filter(vehicles__isnull=False).first()
        vehicles_ids = list(user.vehicles.values_list('id', flat=True))  # "list" to force query execution
        user.delete()

        self.assertTrue(Vehicle.objects.filter(owner__isnull=True, id__in=vehicles_ids).exists())

    def test_delete_replies_on_delete(self):
        user = User.objects.filter(vehicles__occurrences__replies__isnull=False).first()
        replies_ids = list(Reply.objects.filter(occurrence__vehicle__owner=user).values_list('id', flat=True))
        user.delete()

        self.assertFalse(Reply.objects.filter(id__in=replies_ids).exists())

    def test_user_methods(self):
        user = User.objects.first()

        with self.assertRaises(NotImplementedError):
            user.get_full_name()

        with self.assertRaises(NotImplementedError):
            user.get_short_name()


class VehicleOwnershipRequestTestCase(TestCase):
    fixtures = ['users', 'vehicles', 'vehicle_ownership_requests']

    def test_accept_request_with_more_than_one_for_a_vehicle(self):
        vehicle = (Vehicle.objects.annotate(requests_count=Count('ownership_requests'))
                   .filter(requests_count__gt=1, owner__isnull=True,
                           ownership_requests__status=VehicleOwnershipRequest.PENDING_STATUS).first())
        request = vehicle.ownership_requests.first()
        request_count = vehicle.ownership_requests.count()

        request.accept()

        self.assertTrue(VehicleOwnershipRequest.objects
                        .filter(id=request.id, status=VehicleOwnershipRequest.ACCEPTED_STATUS).exists())
        self.assertTrue(Vehicle.objects.filter(id=request.vehicle.id, owner=request.user).exists())
        self.assertTrue(
            request_count - 1,
            vehicle.ownership_requests.filter(status=VehicleOwnershipRequest.DENIED_STATUS).count()
        )

    def test_request_creation_with_owned_vehicle(self):
        vehicle = Vehicle.objects.filter(owner__isnull=False).select_related('owner').first()
        user = User.objects.exclude(id=vehicle.owner.id).first()

        with self.assertRaises(ValidationError) as context_manager:
            VehicleOwnershipRequest.objects.create(vehicle=vehicle, user=user)

        self.assertEqual(context_manager.exception.message, _('The vehicle requested already have an owner.'))
