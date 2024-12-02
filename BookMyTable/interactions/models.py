from django.db import models
from django.conf import settings
from restaurant.models import Restaurant 


# REVIEWS CLASS
class Review(models.Model):
    
    review_id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(max_length=1000, blank=True)


    # using this to configure the details of models database
    class Meta:
        unique_together = ('user', 'restaurant')       # A user can leave only one review per restaurant
        ordering = ['-review_id']


    def __str__(self):
        return f"Review by {self.user} for {self.restaurant} ({self.rating} stars)"


    def update_review(self, rating, comment):
        self.rating = rating
        self.comment = comment
        self.save()



# SAVED RESTAURANTS CLASS
class SavedRestaurant(models.Model):
   
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_restaurants')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')              # A restaurant can only be saved once per user
        ordering = ['saved_at']


    def __str__(self):
        return f"{self.user} saved {self.restaurant}"


    def remove_saved_restaurant(self):
        self.delete()
