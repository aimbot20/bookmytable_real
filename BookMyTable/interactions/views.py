from django.shortcuts import render, get_object_or_404, redirect
from .models import Review, SavedRestaurant
from restaurant.models import Restaurant

# to add a review
def add_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, R_ID=restaurant_id)

    if request.method == "POST":

        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        
        # Check if  user has already reviewed the restaurant
        review, created = Review.objects.get_or_create(
            user=request.user,
            restaurant=restaurant,
            defaults={"rating": rating, "comment": comment}
        )
        
        if not created:
            # If the review already exists, pass error message to template
            return render(request, "interactions/add_review.html", {
                'restaurant': restaurant,
                'user_id': request.user.id,
                'error_message': "You have already reviewed this restaurant!"
            })
        
        # Successfully created a review
        return render(request, "interactions/add_review.html", {
            'restaurant': restaurant,
            'user_id': request.user.id,
            'success_message': "Review added successfully!"
        })

    # Render the form for adding a review if it's a GET request
    return render(request, "interactions/add_review.html", {
        'restaurant': restaurant, 
        'user_id': request.user.id
    })



# to edit a review
def edit_review(request, review_id):
    # Fetch the review or raise a 404 if not found
    review = get_object_or_404(Review, review_id=review_id, user=request.user)

    if request.method == "POST":
        # Extract updated details from the request
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        # Update review details
        review.rating = rating
        review.comment = comment
        review.save()

        return redirect('my_review')
    # Render the edit form with current review data for GET request
    return render(request, "interactions/edit_review.html", {"review": review})


# to delete a review
def delete_review(request, review_id):
    review = get_object_or_404(Review, review_id=review_id, user=request.user)
    review.delete()

    return redirect('my_review')



# to view reviews
def view_reviews(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, R_ID=restaurant_id)
    reviews = restaurant.reviews.all()

    return render(request, "interactions/view_reviews.html", {
        "restaurant": restaurant,
        "reviews": reviews
    })


# to save a restaurant
def save_restaurant(request, restaurant_id):
    if request.user.is_authenticated:
        restaurant = get_object_or_404(Restaurant, R_ID=restaurant_id)
        # Check if the restaurant is already saved by the user
        saved_restaurant, created = SavedRestaurant.objects.get_or_create(
            user=request.user, restaurant=restaurant)
        
        # Redirect back to the restaurant details page
        return redirect('restaurant_details', R_ID=restaurant_id)
    else:
        # Optionally, handle the case where the user is not logged in
        return redirect('login')  # Redirect to login page if not logged in
    

# to remove a saved restaurant
def remove_saved_restaurant(request, saved_id):
    if request.user.is_authenticated:
        # Fetch the saved restaurant record for the current user
        saved_restaurant = get_object_or_404(SavedRestaurant, id=saved_id, user=request.user)
        
        # Remove the saved restaurant
        saved_restaurant.remove_saved_restaurant()
        
        # Redirect to the saved restaurants page
        return redirect('interactions:list_saved_restaurants')
    else:
        return redirect('login')
    

# to view all saved restaurants
def list_saved_restaurants(request):
    if request.user.is_authenticated:
        # Fetch the saved restaurants for the current logged-in user
        saved_restaurants = SavedRestaurant.objects.filter(user=request.user)
        
        # Render the template with saved restaurants
        return render(request, 'interactions/saved_restaurants.html', {'saved_restaurants': saved_restaurants})
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')
    

# to search
def search_restaurant(request):
    query = request.GET.get('q', '')
    restaurants = Restaurant.objects.filter(R_Name__icontains=query)  # Filter restaurants based on search query
    
    # Debugging: print to check if the data is correct
    print(f"Search query: {query}, Found {restaurants.count()} restaurants.")

    return render(request, 'interactions/search_restaurants.html', {
        'restaurants': restaurants
    })