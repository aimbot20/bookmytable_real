from django.shortcuts import render, get_object_or_404
from .models import Menu, Dish, Restaurant, Table, Layout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RestaurantForm, MenuForm, DishForm


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


# Logic building time: 
# After sign up/log in, an owner will be redirected to the owner's dashboard.
# There they will find a Create Restaurant button which will redirect them to add_restaurant
# Add_restaurant will take in the restaurant's details and have a add_menu button
# Add_menu will take in menu details + Dishes + Save button
# Clicking the save button will redirect the owner to their dashboard
# The dashboard will no longer have a "Create Restaurant" button but rather a Edit Restaurant button









def add_or_edit_restaurant(request):
    if not request.user.is_owner:
        return redirect('home')

    owner = request.user.owner
    restaurant = Restaurant.objects.filter(owner=owner).first()

    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = owner
            restaurant.save()
            return redirect('owner_dashboard')
    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, 'restaurant/add_edit_restaurant.html', {'form': form})


def addRestaurantView(request): 
    # if not request.user.is_owner:
    #     return redirect('restaurant_list')

    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user.owner
            restaurant.save()
            return redirect('restaurant_dashboard')
    else:
        form = RestaurantForm()
    return render(request, 'restaurant/add_restaurant.html', {'form':form}) 


def add_menu(request):
    # if not request.user.is_owner:
    #     return redirect('home')

    owner = request.user.owner
    restaurant = Restaurant.objects.filter(owner=owner).first()
    if not restaurant:
        return redirect('add_or_edit_restaurant')  # Ensure restaurant exists first

    menu, created = Menu.objects.get_or_create(restaurant=restaurant)

    if request.method == 'POST':
        # Handle dish addition
        form = DishForm(request.POST)
        if form.is_valid():
            dish = form.save(commit=False)
            dish.menu = menu
            dish.save()

            menu.M_TotalItems += 1
            menu.save()  # Save the updated menu object
            return redirect('add_menu')  # Refresh the menu page
    else:
        form = DishForm()

    dishes = menu.dishes.all() if menu else []
    context = {
        'menu': menu,
        'form': form,
        'dishes': dishes,
        'total_items': menu.M_TotalItems
    }
    return render(request, 'restaurant/add_menu.html', context)




def restaurant_dashboard(request):
    # Fetch the restaurant owned by the logged-in owner
    restaurant = Restaurant.objects.get(owner=request.user.owner)
    return render(request, 'restaurant_dashboard.html', {'restaurant': restaurant})

def menu_dashboard(request):
    # Fetch the menu for the restaurant
    restaurant = Restaurant.objects.get(owner=request.user.owner)
    menu = restaurant.menu  # Assuming a one-to-one relationship
    dishes = menu.dishes.all()  # Fetch all dishes in the menu
    return render(request, 'menu_dashboard.html', {'menu': menu, 'dishes': dishes})
