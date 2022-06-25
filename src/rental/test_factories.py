from . import models as db
import factory


class RentalTestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = db.Rental

    name = factory.Faker("name")


class ReservationTestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = db.Reservation

    rental = factory.SubFactory(RentalTestFactory)
    checkin = factory.Faker("date")
    checkout = factory.Faker("date")
