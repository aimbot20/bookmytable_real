from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Customer, Owner
from .models import Users  # Make sure this is correctly imported
# from django.contrib.auth import login
from restaurant.models import Restaurant
from django.contrib.auth.hashers import check_password
from reservation.models import Reservation
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def home(request):
    # Get the user ID from the query parameters
    user_id = request.GET.get('user_id')
    user = None

    # If user_id is provided, get the user object
    if user_id:
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            user = None
    
    return render(request, 'website/index.html', {'user': user})  # Pass the user to the template


# Landing page: Select user type
def select_user_type(request):
    return render(request, 'users/select_user_type.html')

# Page to select action: Login or Signup
def select_action(request, user_type):
    if user_type not in ['customer', 'owner']:
        return redirect('select_user_type')
    return render(request, 'users/select_action.html', {'user_type': user_type})

# Signup view
def signup(request, user_type):
    if user_type not in ['customer', 'owner']:
        return redirect('select_user_type')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')

        if user_type == 'customer':
            customer = Customer.objects.create_user(
                username=username,
                email=email,
                password=password,
                contact_number=contact_number,
                is_customer=True
            )
            login(request, customer)
            # Redirect to the main app's homepage with the customer ID in the query
            return redirect(reverse('home') + f'?user_id={customer.id}')

        elif user_type == 'owner':
            owner = Owner.objects.create_user(
                username=username,
                email=email,
                password=password,
                contact_number=contact_number,
                is_owner=True
            )
            login(request, owner)
            return redirect('owner_dashboard')  # Redirect to user type selection after signup

    return render(request, f'users/signup_{user_type}.html')


def login_view(request, user_type):
    if user_type not in ['customer', 'owner']:
        return redirect('select_user_type')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Retrieve the user by username
            user = Users.objects.get(username=username)

            # Use check_password to compare the plain password with the hashed password
            if check_password(password, user.password):  # This correctly compares the plain password to the hashed password
                print(f"Password is correct for user: {username}")

                # Password is correct, log the user in
                login(request, user)

                # Redirect based on user type
                if user_type == 'customer' and user.is_customer:
                    return redirect(reverse('home') + f'?user_id={user.id}')
                elif user_type == 'owner' and user.is_owner:
                    return redirect('owner_dashboard')  # Change as necessary
                else:
                    return render(
                        request,
                        f'users/login_{user_type}.html',
                        {'error': 'Invalid user type!', 'user_type': user_type}
                    )
            else:
                # Invalid password
                return render(
                    request,
                    f'users/login_{user_type}.html',
                    {'error': 'Invalid credentials!', 'user_type': user_type}
                )

        except Users.DoesNotExist:
            # User does not exist
            return render(
                request,
                f'users/login_{user_type}.html',
                {'error': 'Invalid credentials!', 'user_type': user_type}
            )

    return render(request, f'users/login_{user_type}.html')



def owner_dashboard(request):
    # if the person requesting this view is not an owner
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated
    
    if not hasattr(request.user, 'owner'):
        return redirect('home')  # Redirect to home if the user is not an owner
    

    # Save the owner in a variable
    owner = request.user.owner 

    # Get the restaurant from the db that belongs to the owner
    restaurant = Restaurant.objects.filter(owner=owner).first()
    
    #restaurant = get_object_or_404(Restaurant, owner=request.user)
    #return render(request, 'your_template.html', {'restaurant': restaurant})

    context = {'restaurant': restaurant, }
    return render(request, 'users/owner_dashboard.html', context)

@login_required
def profile(request):
    user = request.user 

    # Initialize a dictionary to store profile data
    profile_data = {
        'username': user.username,
        'email': user.email,
        'contact_number': None,  # We'll set this based on the user type
    }

    # Check if the user is a Customer
    if hasattr(user, 'customer'):
        # Fetch customer-specific data
        profile_data['contact_number'] = user.customer.contact_number

    # Check if the user is an Owner
    elif hasattr(user, 'owner'):
        # Fetch owner-specific data
        profile_data['contact_number'] = user.owner.contact_number

    return render(request, 'users/profile.html', {'profile_data': profile_data})


#logging out
def logout_view(request):
    logout(request)  
    return redirect('select_user_type')


#my reservations
@login_required
def my_reservations(request):
    user = request.user

    if user.is_customer:
        reservations = Reservation.objects.filter(customer=user)
    elif user.is_owner:
        reservations = Reservation.objects.filter(restaurant__owner=user)
    else:
        reservations = []

    return render(request, 'users/my_reservations.html', {'reservations': reservations})
