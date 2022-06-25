from django.db import models


class Rental(models.Model):
    name = models.CharField(max_length=255)


class Reservation(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    checkin = models.DateField()
    checkout = models.DateField()
