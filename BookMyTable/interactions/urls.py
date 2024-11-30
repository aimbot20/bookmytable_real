from django.urls import path
from . import views  # Import views from the app

urlpatterns = [
    # Example path
    path('', views.home, name='interactions_home'),  # Replace 'home' with your actual view
]