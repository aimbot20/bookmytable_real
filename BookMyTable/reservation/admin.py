from django.contrib import admin

# Register your models here.

from .models import Reservation



class ReservationAdmin(admin.ModelAdmin):
    # Customizing the admin interface for Reservation
    list_display = ('customer', 'restaurant', 'starting_time', 'ending_time', 'reservation_status')
    list_filter = ('reservation_status',)  # Filter by reservation status
    search_fields = ('customer__username', 'restaurant__name')  # Search by customer username or restaurant name



admin.site.register(Reservation, ReservationAdmin)

