import pytest
from .models import Rental, Reservation
from .test_factories import RentalTestFactory, ReservationTestFactory
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
import datetime
from .views import list_of_reservations_with_previous_records


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
    with django_assert_num_queries(1): # Assert that we don't do multiple queries to db
        qs = list_of_reservations_with_previous_records()
        lst = list(qs)

        assert len(lst) == 5
        assert lst[0].checkin == datetime.date(2022, 1, 1)
        assert lst[0].rental_name == 'Rental-1'
        assert lst[0].previous_reservation_id is None

    

@pytest.mark.django_db
def test_get_reservations_with_previous_reservations_from_endpoint(example_data, client, django_assert_num_queries):
    # end desired result:
    # |Rental_name|ID      |Checkin    |Checkout  |Previous reservation, ID|
    # |rental-1   |Res-1 ID| 2022-01-01|2022-01-13| -                      |
    # |rental-1   |Res-2 ID| 2022-01-20|2022-02-10| Res-1 ID               |
    # |rental-1   |Res-3 ID| 2022-02-20|2022-03-10| Res-2 ID               |
    # |rental-2   |Res-4 ID| 2022-01-02|2022-01-20| -                      |
    # |rental-2   |Res-5 ID| 2022-01-20|2022-01-11| Res-4 ID               |
    with django_assert_num_queries(1):
        url = reverse(viewname="previous_reservations")
        responce = client.get(url)
        result = responce.json()

        assert url == "/api/reservations"
        
        assert len(result) == 5
        assert {
            'checkin': '2022-01-01',
            'checkout': '2022-01-13',
            'id': 1,
            'previous_reservation_id': None,
            'rental_name': 'Rental-1'
        } in result
        assert {
            'checkin': '2022-01-20',
            'checkout': '2022-02-10',
            'id': 2,
            'previous_reservation_id': 1,
            'rental_name': 'Rental-1'
        } in result
        assert {
            'checkin': '2022-02-20',
            'checkout': '2022-03-10',
            'id': 3,
            'previous_reservation_id': 2,
            'rental_name': 'Rental-1'
        } in result
        assert {
            'checkin': '2022-01-02',
            'checkout': '2022-01-20',
            'id': 4,
            'previous_reservation_id': None,
            'rental_name': 'Rental-2'
        } in result
        assert {
            'checkin': '2022-01-20',
            'checkout': '2022-02-11',
            'id': 5,
            'previous_reservation_id': 4,
            'rental_name': 'Rental-2'
        } in result





    

