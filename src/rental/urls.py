from . import views
from django.urls import path

urlpatterns = [
    path(
        "reservations",
        views.PreviousReservationsView.as_view(),
        name="previous_reservations",
    ),
]
