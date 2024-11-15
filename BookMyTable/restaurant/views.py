from django.shortcuts import render
from .models import Menu
from .models import Dish
from .models import Restaurant
from .models import Table
from .models import Layout
from .models import Component
from django.shortcuts import get_object_or_404

# # Create your views here.
def restaurant_list(request): 
    restaurants = Restaurant.objects.all() # --> this will all the menu objects and give them in aan array
    return render(request, 'restaurant/all_restaurant.html', {'restaurant_list': restaurants})



# View for restaurant details with dishes
def restaurant_details(request, R_ID):
    restaurant = get_object_or_404(Restaurant, pk=R_ID)
    menu = Menu.objects.filter(restaurant=restaurant).first()  # Assuming one menu per restaurant
    dishes = Dish.objects.filter(menu=menu) if menu else []  # Get dishes for the menu if it exists

    print(f"Restaurant: {restaurant}")
    print(f"Menu: {menu}")
    print(f"Dishes: {list(dishes)}")

    return render(request, 'restaurant/restaurant_details.html', {
        'restaurant': restaurant,
        'dishes': dishes
    })



def reserve_table(request, R_ID):
    restaurant = get_object_or_404(Restaurant, pk=R_ID)
    layout = Layout.objects.filter(restaurant=restaurant).first()
    
    # Retrieve tables associated with the layout
    tables = Table.objects.filter(layout=layout) if layout else []

    return render(request, 'restaurant/reserve_table.html', {
        'restaurant': restaurant,
        'tables': tables,
    })