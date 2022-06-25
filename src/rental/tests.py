import pytest
from .models import Rental, Reservation
from .test_factories import RentalTestFactory, ReservationTestFactory
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
import datetime
from .views import queryset_of_reservations_with_previous_records
from types import SimpleNamespace


@pytest.fixture
def example_data():
    ns = SimpleNamespace(rentals=[], reservations=[])
    ns.rentals = [
        RentalTestFactory(name="Rental-1"),
        RentalTestFactory(name="Rental-2"),
    ]

    ns.reservations = [
        ReservationTestFactory(
            rental=ns.rentals[0], checkin="2022-01-01", checkout="2022-01-13"
        ),
        ReservationTestFactory(
            rental=ns.rentals[0], checkin="2022-01-20", checkout="2022-02-10"
        ),
        ReservationTestFactory(
            rental=ns.rentals[0], checkin="2022-02-20", checkout="2022-03-10"
        ),
        ReservationTestFactory(
            rental=ns.rentals[1], checkin="2022-01-02", checkout="2022-01-20"
        ),
        ReservationTestFactory(
            rental=ns.rentals[1], checkin="2022-01-20", checkout="2022-02-11"
        ),
    ]
    return ns


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

        reservations = example_data.reservations
        rentals = example_data.rentals
        assert len(result) == 5
        assert {
            "checkin": reservations[0].checkin,
            "checkout": reservations[0].checkout,
            "id": reservations[0].id,
            "previous_reservation_id": None,
            "rental_name": rentals[0].name,
        } in result
        assert {
            "checkin": reservations[1].checkin,
            "checkout": reservations[1].checkout,
            "id": reservations[1].id,
            "previous_reservation_id": reservations[0].id,
            "rental_name": rentals[0].name,
        } in result
        assert {
            "checkin": reservations[2].checkin,
            "checkout": reservations[2].checkout,
            "id": reservations[2].id,
            "previous_reservation_id": reservations[1].id,
            "rental_name": rentals[0].name,
        } in result
        assert {
            "checkin": reservations[3].checkin,
            "checkout": reservations[3].checkout,
            "id": reservations[3].id,
            "previous_reservation_id": None,
            "rental_name": rentals[1].name,
        } in result
        assert {
            "checkin": reservations[4].checkin,
            "checkout": reservations[4].checkout,
            "id": reservations[4].id,
            "previous_reservation_id": reservations[3].id,
            "rental_name": rentals[1].name,
        } in result
