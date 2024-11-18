from django.shortcuts import render, get_object_or_404
from .models import Menu, Dish, Restaurant, Table, Layout

def restaurant_list(request):
    user_id = request.GET.get('user_id')  # Capture the user_id from the query parameter
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant/all_restaurant.html', {
        'restaurant_list': restaurants,
        'user_id': user_id  # Pass user_id to the template
    })

# def restaurant_details(request, R_ID):
#     user_id = request.GET.get('user_id')  # Capture user_id from the query parameter
#     restaurant = get_object_or_404(Restaurant, pk=R_ID)
#     menu = Menu.objects.filter(restaurant=restaurant).first()
#     dishes = Dish.objects.filter(menu=menu) if menu else []

#     return render(request, 'restaurant/restaurant_details.html', {
#         'restaurant': restaurant,
#         'dishes': dishes,
#         'user_id': user_id  # Pass user_id to the template
#     })

def restaurant_details(request, R_ID):
    print(f"R_ID: {R_ID}, Query Params: {request.GET}")
    user_id = request.GET.get('user_id')  # Capture user_id from the query parameter
    restaurant = get_object_or_404(Restaurant, pk=R_ID)
    menu = Menu.objects.filter(restaurant=restaurant).first()
    dishes = Dish.objects.filter(menu=menu) if menu else []

    return render(request, 'restaurant/restaurant_details.html', {
        'restaurant': restaurant,
        'dishes': dishes,
        'user_id': user_id
    })


def reserve_table(request, R_ID):
    user_id = request.GET.get('user_id')  # Capture user_id from the query parameter
    restaurant = get_object_or_404(Restaurant, pk=R_ID)
    layout = Layout.objects.filter(restaurant=restaurant).first()
    tables = Table.objects.filter(layout=layout) if layout else []

    return render(request, 'restaurant/reserve_table.html', {
        'restaurant': restaurant,
        'tables': tables,
        'user_id': user_id  # Pass user_id to the template
    })
