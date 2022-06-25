import pytest
from . import models as db
from .test_factories import RentalTestFactory, ReservationTestFactory

@pytest.fixture
def example_data():
    rental_1 = RentalTestFactory(name="Rental-1")
    rental_2 = RentalTestFactory(name="Rental-2")

    ReservationTestFactory(rental=rental_1, checkin="2022-01-01", checkout="2022-01-13")
    ReservationTestFactory(rental=rental_1, checkin="2022-01-20", checkout="2022-02-10")
    ReservationTestFactory(rental=rental_1, checkin="2022-02-20", checkout="2022-03-10")

    ReservationTestFactory(rental=rental_2, checkin="2022-01-02", checkout="2022-01-20")
    ReservationTestFactory(rental=rental_2, checkin="2022-01-20", checkout="2022-02-11")

@pytest.mark.django_db
def test_to_fill_db(example_data):

    assert db.Rental.objects.count() == 2
    assert db.Reservation.objects.count() == 5


    

