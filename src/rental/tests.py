import pytest
from .models import Rental, Reservation
from .test_factories import RentalTestFactory, ReservationTestFactory
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
import datetime
from .views import queryset_of_reservations_with_previous_records


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
    with django_assert_num_queries(
        1
    ):  # Ensuring we do only one SQL request to database
        qs = queryset_of_reservations_with_previous_records()
        lst = list(qs)

        assert len(lst) == 5
        assert lst[0].checkin == datetime.date(2022, 1, 1)
        assert lst[0].rental.name == "Rental-1"
        assert lst[0].previous_reservation_id is None


@pytest.mark.django_db
def test_get_reservations_with_previous_reservations_from_endpoint(
    example_data, client, django_assert_num_queries
):
    with django_assert_num_queries(1):
        url = reverse(viewname="previous_reservations")
        responce = client.get(url)
        result = responce.json()

        assert url == "/api/reservations"

        from pprint import pprint as print

        print(result)

        assert len(result) == 5
        assert {
            "checkin": "2022-01-01",
            "checkout": "2022-01-13",
            "id": 1,
            "previous_reservation_id": None,
            "rental_name": "Rental-1",
        } in result
        assert {
            "checkin": "2022-01-20",
            "checkout": "2022-02-10",
            "id": 2,
            "previous_reservation_id": 1,
            "rental_name": "Rental-1",
        } in result
        assert {
            "checkin": "2022-02-20",
            "checkout": "2022-03-10",
            "id": 3,
            "previous_reservation_id": 2,
            "rental_name": "Rental-1",
        } in result
        assert {
            "checkin": "2022-01-02",
            "checkout": "2022-01-20",
            "id": 4,
            "previous_reservation_id": None,
            "rental_name": "Rental-2",
        } in result
        assert {
            "checkin": "2022-01-20",
            "checkout": "2022-02-11",
            "id": 5,
            "previous_reservation_id": 4,
            "rental_name": "Rental-2",
        } in result
