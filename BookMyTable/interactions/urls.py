from django.urls import path
from . import views  # Import views from the app

app_name = 'interactions'

urlpatterns = [
    
   path('add_review/<int:restaurant_id>/', views.add_review, name='add_review'),

   path('edit-review/<int:review_id>/', views.edit_review, name='edit_review'),

   path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),

   path('save-restaurant/<int:restaurant_id>/', views.save_restaurant, name='save_restaurant'),
 
   path('remove-saved-restaurant/<int:saved_id>/', views.remove_saved_restaurant, name='remove_saved_restaurant'),
 
   path('saved-restaurants/', views.list_saved_restaurants, name='list_saved_restaurants'),
   
   path('search/', views.search_restaurant, name='search_restaurant'),
   
]
