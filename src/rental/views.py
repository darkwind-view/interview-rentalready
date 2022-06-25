from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework import generics
from .models import Reservation

# |Rental_name|ID      |Checkin    |Checkout  |Previous reservation, ID|
# |rental-1   |Res-1 ID| 2022-01-01|2022-01-13| -                      |
# |rental-1   |Res-2 ID| 2022-01-20|2022-02-10| Res-1 ID               |
# |rental-1   |Res-3 ID| 2022-02-20|2022-03-10| Res-2 ID               |
# |rental-2   |Res-4 ID| 2022-01-02|2022-01-20| -                      |
# |rental-2   |Res-5 ID| 2022-01-20|2022-01-11| Res-4 ID               |


class PreviousReservationsQueryset(QuerySet):
    pass


class PreviousReservationsSerializer(serializers.ModelSerializer):
    rental_name = serializers.CharField(source="rental.name")

    class Meta:
        model = Reservation
        fields = [
            'rental_name',
            'id',
            'checkin',
            'checkout',
        ]

class PreviousReservationsView(generics.ListAPIView):
    queryset = Reservation.objects.all().select_related("rental")
    serializer_class = PreviousReservationsSerializer