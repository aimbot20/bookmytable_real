from django.shortcuts import render, get_object_or_404, redirect
from restaurant.models import Restaurant, Table, Layout  # Add Layout import here
from .models import Reservation
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.http import HttpResponse

@login_required
def select_time(request, R_ID):
    # Get the restaurant object
    restaurant = get_object_or_404(Restaurant, pk=R_ID)
    
    if request.method == "POST":
        # Get the selected time from the form
        start_time = request.POST.get('start_time')
        
        request.session['start_time'] = start_time
        # Redirect to the show_tables view, passing the restaurant and selected time
        return redirect('reservation:show_tables', R_ID=R_ID, start_time=start_time)
    
    # Available hours (you can adjust this based on your needs)
    available_hours = ['1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM']

    return render(request, 'reservation/select_time.html', {
        'restaurant': restaurant,
        'available_hours': available_hours
    })



# -------------->> ARHAM'S WORKING CODE RAHHHHHHH <<------------------------
def show_tables(request, R_ID, start_time):

    # Get the restaurant object
    restaurant = get_object_or_404(Restaurant, pk=R_ID)

    # Convert start_time to a datetime object
    try:
        start_time_obj = datetime.strptime(start_time, '%I %p')  # e.g., '4 PM' -> 16:00
    except ValueError:
        return HttpResponse("Invalid time format", status=400)

    # Get the layout associated with the restaurant
    layout = get_object_or_404(Layout, restaurant=restaurant)

    # Get all tables associated with the layout
    all_tables = Table.objects.filter(layout=layout)

    # Separate tables into available and reserved lists
    available_tables = []
    reserved_tables = []

    for table in all_tables:
    # Check if the table has any confirmed reservations with the same starting time
        conflicting_reservations = Reservation.objects.filter(
            table=table,
            reservation_status="Confirmed",
            starting_time=start_time_obj
        )

        if conflicting_reservations.exists():
            reserved_tables.append(table)  # Add to reserved tables
        else:
            available_tables.append(table)  # Add to available tables


    # print the two lists here 
    print("Available Tables:", [f"Table ID: {t.T_ID}, Capacity: {t.T_SeatingCapacity}" for t in available_tables])
    print("Reserved Tables:", [f"Table ID: {t.T_ID}, Capacity: {t.T_SeatingCapacity}" for t in reserved_tables])
   
   
    # Handle POST request for table reservation
    if request.method == 'POST':
        table_id = request.POST.get('table_id')
        if not table_id:
            return HttpResponse("No table ID provided", status=400)
    

        table = get_object_or_404(Table, pk=table_id)

        # Check if the table is in the reserved list
        if table in reserved_tables:
            return HttpResponse("This table is already reserved at the requested time. Please select another.", status=400)

        # Create the reservation
        reservation = Reservation.objects.create(
            customer=request.user.customer,  # Access the customer object from the user
            restaurant=restaurant,
            table=table,
            starting_time=start_time_obj,
            ending_time=start_time_obj + timedelta(minutes=59),  # Example duration
            reservation_status="Pending",
        )

        # Redirect to payment page
        return redirect('payment_page', R_ID=R_ID, T_ID=table.T_ID, reservation_id=reservation.id)

    # Pass categorized tables to the template
    return render(request, 'reservation/show_tables.html', {
        'restaurant': restaurant,
        'start_time': start_time_obj.strftime('%I:%M %p'),
        'available_tables': available_tables,
        'reserved_tables': reserved_tables,
        'layout': layout,
    })

