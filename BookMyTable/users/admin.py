from django.contrib import admin
from .models import Users, Owner, Customer

# Inline for Customer

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'contact_number', 'wallet_balance')

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('username', 'business_name', 'contact_number')
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email', 'first_name', 'last_name', 'contact_number', 'business_name')
        }),
    )

# Register the admin for Users, Customer, and Owner

admin.site.register(Customer, CustomerAdmin)  # Register the Customer model separately if needed
admin.site.register(Owner, OwnerAdmin)     # Register the Owner model separately if needed
admin.site.register(Users)



#-------------------------------------------------------------------------------------


# class CustomerInline(admin.StackedInline):
#     model = Customer
#     can_delete = False
#     verbose_name_plural = 'Customer Details'
#     extra = 1  # This defines how many blank forms to show when adding a new user

# # Inline for Owner
# class OwnerInline(admin.StackedInline):
#     model = Owner
#     can_delete = False
#     verbose_name_plural = 'Owner Details'
#     extra = 1

# # Customizing the UserAdmin to show Customer/Owner inlines based on User's attributes
# class UsersAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_customer', 'is_owner')
    
#     def get_inline_instances(self, request, obj=None):
#         inlines = []
#         if obj:
#             if obj.is_customer:
#                 inlines.append(CustomerInline(self.model, self.admin_site))
#             if obj.is_owner:
#                 inlines.append(OwnerInline(self.model, self.admin_site))
#         return inlines

#admin.site.register(Users, UsersAdmin)