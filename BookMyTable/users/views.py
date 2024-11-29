from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .models import Customer, Owner
from .models import Users  # Make sure this is correctly imported
# from django.contrib.auth import login
from restaurant.models import Restaurant
from django.contrib.auth.hashers import check_password

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
    
    # if not request.user.is_owner: 
    #     # Tell them to fuck off
    #     return redirect('home')
    



    # Save the owner in a variable
    owner = request.user.owner 

    # Get the restaurant from the db that belongs to the owner
    restaurant = Restaurant.objects.filter(owner=owner).first()

    context = {'restaurant': restaurant, }
    return render(request, 'users/owner_dashboard.html', context)

