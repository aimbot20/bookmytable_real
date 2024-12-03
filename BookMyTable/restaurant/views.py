from django.shortcuts import render, get_object_or_404
from .models import Menu, Dish, Restaurant, Table, Layout, Door, Window, Component
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import RestaurantForm, MenuForm, DishForm, LayoutForm
from django.http import JsonResponse
import json
from interactions.models import Review


def restaurant_list(request):
    user_id = request.GET.get('user_id')  # Capture the user_id from the query parameter
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant/all_restaurant.html', {
        'restaurant_list': restaurants,
        'user_id': user_id  # Pass user_id to the template
    })


def restaurant_details(request, R_ID):
    print(f"R_ID: {R_ID}, Query Params: {request.GET}")
    user_id = request.GET.get('user_id')  # Capture user_id from the query parameter
    restaurant = get_object_or_404(Restaurant, pk=R_ID)
    
    # Fetch menu and dishes
    menu = Menu.objects.filter(restaurant=restaurant).first()
    dishes = Dish.objects.filter(menu=menu) if menu else []

    # Fetch reviews for the restaurant
    reviews = Review.objects.filter(restaurant=restaurant)

    return render(request, 'restaurant/restaurant_details.html', {
        'restaurant': restaurant,
        'dishes': dishes,
        'reviews': reviews,  # Pass reviews to the template
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




def save_layout(request, layout_id):
    layout = Layout.objects.get(id=layout_id)

    if request.method == 'POST':
        components = request.POST.get('components')  # Expect JSON data
        for comp in components:
            if comp['type'] == 'table':
                Table.objects.update_or_create(
                    id=comp.get('id'),
                    defaults={
                        'layout': layout,
                        'x_position': comp['x'],
                        'y_position': comp['y'],
                        'seating_capacity': comp['seating_capacity'],
                        'color': comp['color']
                    }
                )
            elif comp['type'] == 'door':
                Door.objects.update_or_create(
                    id=comp.get('id'),
                    defaults={
                        'layout': layout,
                        'x_position': comp['x'],
                        'y_position': comp['y'],
                        'length': comp['length']
                    }
                )
            elif comp['type'] == 'window':
                Window.objects.update_or_create(
                    id=comp.get('id'),
                    defaults={
                        'layout': layout,
                        'x_position': comp['x'],
                        'y_position': comp['y'],
                        'length': comp['length']
                    }
                )
    return JsonResponse({'message': 'Layout saved successfully!'})


def manage_layout(request):     #   function definition -making a view, request contains the metadata about the HTTP request (method, data, headers)
    # creating a HTML page for managing the layout: 

    width, height = None, None  #   initializing 2 variables: height and width to later store data
    restaurant = request.user.owner.restaurant  #storing the restaurant associated with the owner

    # If the owner already has a layout, then they won't get any edit functionality and will only be able to see it.
    layout = Layout.objects.filter(restaurant=restaurant).first()
    #components = Component.objects.filter(layout = layout)

    if layout:  # If a layout exists
        # components = restaurant.components.all()  # Includes all associated components (tables, etc.)
        tables = layout.tables.all()  # If you've separated tables specifically
        return render(request, 'restaurant/manage_layout.html', {
            'layout': layout,
            #'components': components,
            'tables': tables,
            'editing_disabled': True  # Pass this flag to the template
        })



    if layout and request.method == 'POST':  # Prevent edits if a layout exists
        return HttpResponseForbidden("Layout editing is not allowed.")




    # We have a form to get the dimensions of the layout, I am adding that here
    if request.method == 'POST':    # if form data is being submitted - i.e. form has been filled

        form = LayoutForm(request.POST)     # this instantiates the form with the submitted data as an instance of the Layout form and stores the info in a variable called form 

        if form.is_valid():     #if the form has been filled correctly according to the fields defined in the LayoutForm
            
            # ----------------------------------------------------
            #Create a layout object using the form data but doesn't save it immediately to the database (so it can be modified)
            layout = form.save(commit=False)
            layout.restaurant = restaurant  # Link the restaurant of the created layout object to our current restaurant
            width = layout.width
            height = layout.height

            layout.save()   # save the layout to the database
            # ----------------------------------------------------

            
            # ----------------------------------------------------
            tables_data = request.POST.get('tables')
            # print(request.POST.get('tables'))  # Check the serialized table data
                
            #If any table_data exists
            if tables_data:
                #convert it from json string to python dictionary
                tables_data = json.loads(tables_data)
                print(tables_data)
                
                for table_data in tables_data:
                        #create a Table object
                        Table.objects.create(
                            #x_position= request.POST.get('x_position'),
                            #y_position= request.POST.get('y_position'),
                            #T_SeatingCapacity= request.POST.get('seating_capacity', 4),
                            x_position = table_data['x_position'],
                            y_position = table_data['y_position'],
                            T_SeatingCapacity= table_data['seating_capacity'],
                            
                            color='blue',
                            layout=layout
                        )

            # ----------------------------------------------------

            return redirect('owner_dashboard')

    #------------------------------------------------------------------------------
         

    else:
        form = LayoutForm()

    layout = Layout.objects.filter(restaurant=restaurant).first()
    tables = Table.objects.filter(layout=layout) if layout else []



    # return render(request, 'restaurant/manage_layout.html', {'form':form, 'width':width, 'height':height})
    return render(request, 'restaurant/manage_layout.html', {
        'form': form,
        'width': width,
        'height': height,
        'tables': tables,
        'editing_disabled': False  # Allow editing if no layout exists
        
    })

def add_tables(request, R_ID): 

    # gets the restaurant which has the ID specified in the url 
    restaurant = get_object_or_404(Restaurant, pk=R_ID)

    #loads a layout if already created or creates a new one
    layout, created = Layout.objects.get_or_create(restaurant=restaurant)  # Create or fetch layout


    #Fetching all tables, doors, and windows related to the layout using Django's ORM.
    tables = Table.objects.filter(layout=layout)
    doors = Door.objects.filter(layout=layout)
    windows = Window.objects.filter(layout=layout)
    components = list(tables) + list(doors) + list(windows)
   
   
    resolved_components = []
        
    for component in components:
        component_type = type(component).__name__.lower()  # Get the class name as a string
        resolved_components.append({
        'id': component.pk,
        'type': component.type,
        'seating_capacity': getattr(component, 'T_SeatingCapacity', None),
        'color': getattr(component, 'color', 'blue'),
        'length': getattr(component, 'W_Length', None),
        'x': component.x_position,
        'y': component.y_position,
        })


    if request.method == 'POST':
        # Extract the list of components from the POST data (components).
        components = request.POST.get('components')  # Logic to handle saving components

        #go over each component
        for comp in components:
            # if the component is a table
            if comp['type'] == 'table':
                Table.objects.update_or_create(
                    id=comp.get('id'),
                    defaults={
                        'layout': layout,
                        'x_position': comp['x'],
                        'y_position': comp['y'],
                        'seating_capacity': comp['seating_capacity'],
                        'color': comp['color']
                    }
                )
        return JsonResponse({'message': 'Tables added successfully!'})

    return render(request, 'restaurant/add_table.html', {
        'restaurant': restaurant,
        'layout': layout,
        'R_ID': R_ID,
        'components': resolved_components,  # Pass processed components
    })


