from django.shortcuts import render
from .models import Menu
from .models import Dish
from .models import Restaurant
from django.shortcuts import get_object_or_404

# Create your views here.
def restaurant_list(request): 
    restaurants = Restaurant.objects.all() # --> this will all the menu objects and give them in aan array
    return render(request, 'restaurant/all_restaurant.html', {'restaurant_list': restaurants})

def restaurant_details(request, R_ID):
    restaurant_details = get_object_or_404(Restaurant, pk = R_ID)
    return render (request, 'restaurant/restaurant_details.html', {'restaurant': restaurant_details})

