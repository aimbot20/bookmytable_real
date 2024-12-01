from django.db import models
from django.utils import timezone


# Create your models here.
  
class Restaurant(models.Model):
    R_ID = models.AutoField(primary_key=True)
    R_Name = models.CharField(max_length=100)
    #One restaurant per owner
    owner = models.OneToOneField('users.Owner', on_delete=models.CASCADE, related_name='restaurant')
    R_EmailAddress = models.EmailField(unique=True)
    R_ContactNumber = models.CharField(unique = True, max_length=15)
    R_Address = models.TextField() # this will allow for multiple addresses too
    R_Description = models.TextField(blank=True, null=True) #can be left blank, will store NULL if no value exists
    R_CuisineTypes = models.CharField(max_length=100)
    R_ReservationCost = models.DecimalField(max_digits=10, decimal_places=2)
    R_OpenHours = models.CharField(max_length=100) # e.g "Mon-Fri: 9:00AM - 8PM"
    Rating = models.DecimalField(decimal_places=2, default=0.0, max_digits=100)
    NetRevenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    # image = models.ImageField(upload_to='restaurantImages/')
    
    def __str__(self):  #this will save the name of a res obj created in admin panel as the name given to it
        return self.R_Name
        
class Menu(models.Model): 
    M_ID = models.AutoField(primary_key = True)
    M_TotalItems = models.IntegerField(null = False, default = 0)
   # restaurant = models.ForeignKey('Restaurant', on_delete = models.CASCADE, related_name = 'menu')

   # I think restaurand and menu have a One-to-One relationship rather than One-to-Many relationship (foreign key)
   # Because one restaurant should only have 1 menu
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name='restaurant')

    def __str__(self):  #this will save the name of a res obj created in admin panel as the name given to it
        return f"{self.restaurant.R_Name} Menu"

class Dish(models.Model):
    D_ID = models.AutoField(primary_key=True)
    # One menu can have many dishes so dish and menu have a One-to-Many relationship
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='dishes')
    D_Name = models.CharField(max_length=100)
    D_Description = models.TextField(blank=True, null=True)
    D_Price = models.DecimalField(decimal_places = 2, default = 0.0, max_digits=100)
    D_PrepTime = models.IntegerField()
    D_Category = models.CharField(max_length = 100) # e.g "BreakFast/Lunch/Dinner/Appetizer/Dessert/MainCourse" 
   # D_DateAdded = models.DateTimeField(default=timezone.now)

    def __str__(self):  #this will save the name of a res obj created in admin panel as the name given to it
        return self.D_Name


class Layout(models.Model):
    #this is a composition relation because the menu will get deleted if the restaurants gets deleted. 
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name='layout') 
    width = models.IntegerField(default= 0)  # Layout width in pixels or grid units
    height = models.IntegerField(default= 0)  # Layout height in pixels or grid units





class Component(models.Model): 
    #This is an abstract class to serve as an interface for different components and allow for Open-Close Principle
    x_position = models.IntegerField(null=True, blank=True, default = 0)
    y_position = models.IntegerField(null=True, blank=True, default = 0)
    layout = models.ForeignKey('Layout', on_delete = models.CASCADE, related_name='components')
    type = models.CharField(max_length=50)
    
    class Meta: 
        abstract = True



#Changes: added a fixed width to Door 
class Table(Component):
    #Defining enumeration class
    TableAvailability = [
        ('red', 'Reserved'),
        ('blue', 'Available'),
        ('yellow', 'Selected')
    ]
    T_ID = models.AutoField(primary_key=True)
    T_SeatingCapacity = models.IntegerField()
    is_reserved = models.BooleanField(default=False)  # Track if the table is reserved
    color = models.CharField(max_length=6, default='blue', choices=TableAvailability)  # Options: 'red', 'blue', 'yellow'
    layout = models.ForeignKey(Layout, on_delete=models.CASCADE, related_name='tables')
    type = models.CharField(max_length=50, default='table', editable=False)

    def __str__(self):
        return f"Table {self.T_ID} - {self.T_SeatingCapacity} seats"




#Changes: added a fixed width to Window the __str__ function
class Window(Component):
    W_Length = models.IntegerField()
    W_Width = models.IntegerField(default = 5)
    layout = models.ForeignKey(Layout, on_delete=models.CASCADE, related_name='windows')
    type = models.CharField(max_length=50, default='window', editable=False)
    
    def __str__(self):
        return f"Door at ({self.x_position}, {self.y_position}) - Length: {self.W_Length}"



#Changes: added a fixed width to Door and a __str__ function
class Door(Component):
    D_Length = models.IntegerField()
    D_Width = models.IntegerField(default = 5)
    layout = models.ForeignKey(Layout, on_delete=models.CASCADE, related_name='doors')
    type = models.CharField(max_length=50, default='door', editable=False)
    
    def __str__(self):
        return f"Door at ({self.x_position}, {self.y_position}) - Length: {self.W_Length}"


class Coordinates(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()


