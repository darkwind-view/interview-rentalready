import pytest
from . import models as db

def test_check():
    assert True


@pytest.mark.django_db
def test_to_view_reservations():
    rental_1 = db.Rental(name="Rental-1")
    rental_2 = db.Rental(name="Rental-2")
    rental_1.save()
    rental_2.save()

    db.Reservation(rental=rental_1, checkin="2022-01-01", checkout="2022-01-13").save()
    db.Reservation(rental=rental_1, checkin="2022-01-20", checkout="2022-02-10").save()
    db.Reservation(rental=rental_1, checkin="2022-02-20", checkout="2022-03-10").save()

    db.Reservation(rental=rental_2, checkin="2022-01-02", checkout="2022-01-20").save()
    db.Reservation(rental=rental_2, checkin="2022-01-20", checkout="2022-02-11").save()