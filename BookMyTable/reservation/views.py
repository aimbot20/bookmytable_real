from django.shortcuts import render, get_object_or_404, redirect
from restaurant.models import Restaurant, Table
from .models import Reservation
from django.contrib.auth.decorators import login_required

@login_required
def reservation_details(request, R_ID, T_ID):
    # Fetch the restaurant and table based on IDs
    restaurant = get_object_or_404(Restaurant, R_ID=R_ID)
    table = get_object_or_404(Table, T_ID=T_ID)

    if request.method == "POST":
        # Create the reservation after confirmation
        starting_time = request.POST.get("starting_time")
        ending_time = request.POST.get("ending_time")

        reservation = Reservation.objects.create(
            customer=request.user.customer,  # Access the customer object from the user
            restaurant=restaurant,
            table=table,
            starting_time=starting_time,
            ending_time=ending_time,
            reservation_status="Pending",
        )
        print(f"Reservation created with ID: {reservation.id}")
        # Redirect to the payment page, passing the reservation ID, restaurant ID, and table ID
        #return redirect('payment_page', R_ID=R_ID, T_ID=T_ID, reservation_id=reservation.id)
        return redirect('payment_page', R_ID=R_ID, T_ID=T_ID, reservation_id=reservation.id)

    
    # For GET, show reservation details page
    return render(request, 'reservation/reservation_details.html', {
        'restaurant': restaurant,
        'table': table,
    })
