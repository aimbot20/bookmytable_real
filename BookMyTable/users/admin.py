from django.contrib import admin
from .models import Owner, Users, Customer

# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('business_name',)
    #inlines = ['UsersAdmin']
    #filter_horizontal = ('first_name', )

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', )
    #inlines = ['UsersAdmin']


# admin.site.register(Owner)
# admin.site.register(Customer)
admin.site.register(Users, UsersAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Customer, CustomerAdmin)
