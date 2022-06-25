import pytest
from .models import Rental, Reservation
from .test_factories import RentalTestFactory, ReservationTestFactory
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from pprint import pprint as print
import datetime

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

    assert Rental.objects.count() == 2
    assert Reservation.objects.count() == 5


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_query_previous_reservations(example_data, client, django_assert_num_queries):
    with django_assert_num_queries(1):
        qs = Reservation.objects.all().select_related("rental")
        lst = list(qs)

        assert len(lst) == 5
        assert lst[0].checkin == datetime.date(2022, 1, 1)
        assert lst[0].rental.name == 'Rental-1'
    

@pytest.mark.django_db
def test_get_view(example_data, client, django_assert_num_queries):
    with django_assert_num_queries(1):
        url = reverse(viewname="previous_reservations")
        responce = client.get(url)
        result = responce.json()

        assert url == "/api/reservations"
        assert result[0]["id"] == 1
        assert result[0]["checkin"] == '2022-01-01'
        assert result[0]["checkout"] == '2022-01-13'
        assert result[0]["rental_name"] == 'Rental-1'

        print(result)




    

