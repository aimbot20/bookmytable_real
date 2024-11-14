from django.shortcuts import render
from .models import Menu
from .models import Dish
from .models import Restaurant
from django.shortcuts import get_object_or_404

# # Create your views here.
def restaurant_list(request): 
    restaurants = Restaurant.objects.all() # --> this will all the menu objects and give them in aan array
    return render(request, 'restaurant/all_restaurant.html', {'restaurant_list': restaurants})

# def restaurant_details(request, R_ID):
#     restaurant_details = get_object_or_404(Restaurant, pk = R_ID)
#     return render (request, 'restaurant/restaurant_details.html', {'restaurant': restaurant_details})

#from django.shortcuts import render, get_object_or_404
#from .models import Menu, Dish, Restaurant

# View for restaurant details with dishes
def restaurant_details(request, R_ID):
    restaurant = get_object_or_404(Restaurant, pk=R_ID)
    menu = Menu.objects.filter(restaurant=restaurant).first()  # Assuming one menu per restaurant
    dishes = Dish.objects.filter(menu=menu) if menu else []  # Get dishes for the menu if it exists
    return render(request, 'restaurant/restaurant_details.html', {
        'restaurant': restaurant,
        'dishes': dishes
    })
