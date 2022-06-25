from rest_framework import serializers
from rest_framework import generics
from .models import Reservation
from django.db.models import Window, F
from django.db.models.functions import Lag


def queryset_of_reservations_with_previous_records():
    # end desired result:
    # |Rental_name|ID      |Checkin    |Checkout  |Previous reservation, ID|
    # |rental-1   |Res-1 ID| 2022-01-01|2022-01-13| -                      |
    # |rental-1   |Res-2 ID| 2022-01-20|2022-02-10| Res-1 ID               |
    # |rental-1   |Res-3 ID| 2022-02-20|2022-03-10| Res-2 ID               |
    # |rental-2   |Res-4 ID| 2022-01-02|2022-01-20| -                      |
    # |rental-2   |Res-5 ID| 2022-01-20|2022-01-11| Res-4 ID               |

    qs = Reservation.objects.select_related("rental").annotate(
        previous_reservation_id=Window(
            expression=Lag("id", 1),
            partition_by=[F("rental_id")],
            order_by=F("rental_id").asc(),
        ),
    )
    return qs


class PreviousReservationsSerializer(serializers.ModelSerializer):
    rental_name = serializers.CharField(source="rental.name")
    previous_reservation_id = serializers.IntegerField()

    class Meta:
        model = Reservation
        fields = [
            "rental_name",
            "id",
            "checkin",
            "checkout",
            "previous_reservation_id",
        ]


class PreviousReservationsView(generics.ListAPIView):
    queryset = queryset_of_reservations_with_previous_records()
    serializer_class = PreviousReservationsSerializer
