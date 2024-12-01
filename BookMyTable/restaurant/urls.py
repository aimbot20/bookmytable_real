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
    path('add-restaurant/', views.add_or_edit_restaurant, name='add_or_edit_restaurant'),
    path('add-menu/', views.add_menu, name='add_menu'),
    path('manage-layout/', views.manage_layout, name='manage_layout'),

    path('<int:R_ID>/add_table/', views.add_tables, name='add_tables'),
    
]