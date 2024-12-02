from django.contrib import admin
from .models import Review, SavedRestaurant

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'user', 'restaurant', 'rating', 'comment')
    list_filter = ('rating', 'restaurant')
    search_fields = ('user__username', 'restaurant__R_Name', 'comment')
    ordering = ('-review_id',)
    readonly_fields = ('review_id',)

@admin.register(SavedRestaurant)
class SavedRestaurantAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'saved_at')
    list_filter = ('saved_at', 'restaurant')
    search_fields = ('user__username', 'restaurant__R_Name')
    ordering = ('-saved_at',)
