from django.db import models
from django.conf import settings  # Import the custom user model
from restaurant.models import Restaurant, Table  # Import necessary models

class Reservation(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_customer': True},  # Ensure only customers can be linked
        related_name="reservations"
    )
    restaurant = models.ForeignKey(
        Restaurant,  # Reference to the restaurant
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    table = models.ForeignKey(
        Table,  # Reference to the selected table
        on_delete=models.CASCADE,
        related_name="reservations",
        default=1 
    )
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    reservation_status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Reservation by {self.customer.username} at {self.restaurant.R_Name}"

