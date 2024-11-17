from django.contrib import admin
# using this file, you can attach your models to admin and view them online
from .models import Restaurant
from .models import Menu
from .models import Dish
from .models import Layout
from .models import Component
from .models import Coordinates
from .models import Table




# Register your models here.


class MenuInLine(admin.StackedInline):
    model = Menu
    extra = 1

class DishInLine(admin.StackedInline):
    model = Dish
    extra = 1

#------------------------------------------


class RestaurantAdmin(admin.ModelAdmin):
    inlines = [MenuInLine]
    # Now u will be able to add a menu while creating a restuarant

     # You can also override the save_model method to automatically create a Menu for the Restaurant
    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     # Automatically create a Menu for the Restaurant if it doesn't already exist
    #     if not hasattr(obj, 'menu'):
    #         Menu.objects.create(restaurant=obj)


class MenuAdmin(admin.ModelAdmin):
    inlines = [DishInLine]
    # With this, u can add dishes through the admin panel while making a menu 
    




admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Layout)
admin.site.register(Component)
admin.site.register(Table)
admin.site.register(Coordinates)



