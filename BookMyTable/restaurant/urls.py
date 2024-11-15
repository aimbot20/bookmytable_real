# All the commented lines are not needed in this file
# from django.contrib import admin
from django.urls import path
from . import views

# localhost: 8000/chai
# localhost: 8000/chai/order
urlpatterns = [
    
    path('', views.restaurant_list, name = 'all_restaurant'),
    path('<int:R_ID>/', views.restaurant_details, name = 'restaurant_details'),
    path('<int:R_ID>/reserve_table/', views.reserve_table, name='reserve_table'),
    
]