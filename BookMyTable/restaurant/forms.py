from django import forms
from .models import Restaurant, Menu, Dish

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['R_Name', 'R_EmailAddress', 'R_ContactNumber', 'R_Address', 
                  'R_Description', 'R_CuisineTypes', 'R_ReservationCost', 'R_OpenHours']

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['M_TotalItems']  # Since Menu doesn't require many direct inputs

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['D_Name', 'D_Description', 'D_Price', 'D_PrepTime', 'D_Category']


        
