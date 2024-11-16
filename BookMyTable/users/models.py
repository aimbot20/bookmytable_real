from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):  # Inherits from Django's AbstractUser
    is_customer = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    # Your custom user fields here
    # Change related_name to avoid clash with the default User model
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Change the related name
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Change the related name
        blank=True,
    )

class Customer(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    wallet_balance = models.FloatField(default=0.0)

    def add_to_wallet(self, amount):
        self.wallet_balance += amount
        self.save()

    def deduct_from_wallet(self, amount):
        if self.wallet_balance >= amount:
            self.wallet_balance -= amount
            self.save()
            return True
        return False

class Owner(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    business_name = models.CharField(max_length=100, blank=True, null=True)

    def get_registered_restaurants(self):
        return self.restaurant_set.all()
