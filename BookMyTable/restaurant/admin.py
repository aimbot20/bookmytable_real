from django.contrib import admin
# using this file, you can attach your models to admin and view them online
from .models import Restaurant
from .models import Menu
from .models import Dish
from .models import Layout
from .models import Component



# Register your models here.
admin.site.register(Menu)
admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(Layout)
admin.site.register(Component)


