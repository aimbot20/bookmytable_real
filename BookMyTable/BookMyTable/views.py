from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import Users

def home(request):
    user_id = request.GET.get('user_id')  # Capture user ID from query parameters
    user = None

    if request.user.is_authenticated:  # Check if the user is logged in
        user = request.user  # Use the logged-in user

    # If user_id is provided in the URL, get the user object for that ID
    if user_id and not user:
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            user = None

    return render(request, 'website/index.html', {'user': user})  # Pass the user to the template
def contact(request):
    user_id = request.GET.get('user_id')  # Capture user_id from query parameters
    return render(request, 'website/contact.html', {'user_id': user_id})

def about(request):
    user_id = request.GET.get('user_id')  # Capture user_id from query parameters
    return render(request, 'website/about.html', {'user_id': user_id})
