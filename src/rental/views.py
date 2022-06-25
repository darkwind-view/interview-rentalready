from rest_framework import serializers
from rest_framework import generics
from .models import Reservation


def list_of_reservations_with_previous_records():
    return  Reservation.objects.raw("""
SELECT rental.name as rental_name, rental.id as rental_id, reservation.id as id, reservation.checkin as checkin, reservation.checkout as checkout, 
LAG(reservation.id, 1) OVER (PARTITION BY reservation.rental_id ORDER BY reservation.rental_id) previous_reservation_id
FROM rental_reservation as reservation
JOIN rental_rental as rental ON rental.id = reservation.rental_id
    """)


class PreviousReservationsSerializer(serializers.ModelSerializer):
    rental_name = serializers.CharField()
    previous_reservation_id = serializers.IntegerField()

    class Meta:
        model = Reservation
        fields = [
            'rental_name',
            'id',
            'checkin',
            'checkout',
            'previous_reservation_id',
        ]

class PreviousReservationsView(generics.ListAPIView):
    queryset = list_of_reservations_with_previous_records()
    serializer_class = PreviousReservationsSerializer