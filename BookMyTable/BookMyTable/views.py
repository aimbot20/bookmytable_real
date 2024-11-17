from django.shortcuts import render, redirect
from django.http import HttpResponse

def home(request):
    user_id = request.GET.get('user_id')  # Capture user_id from query parameters
    return render(request, 'website/index.html', {'user_id': user_id})

def contact(request):
    user_id = request.GET.get('user_id')  # Capture user_id from query parameters
    return render(request, 'website/contact.html', {'user_id': user_id})

def about(request):
    user_id = request.GET.get('user_id')  # Capture user_id from query parameters
    return render(request, 'website/about.html', {'user_id': user_id})
