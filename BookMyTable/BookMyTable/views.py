from django.http import HttpResponse
from django.shortcuts import render

def home(request): 
    #return HttpResponse("Hello, you are now viewing BookMyTable's Homepage.")
    return render(request, 'website/index.html')

def contact(request): 
    return HttpResponse("Hello, you are now viewing BookMyTable's Contact page.")

def about(request): 
    return HttpResponse("Hello, you are now viewing BookMyTable's About page.")