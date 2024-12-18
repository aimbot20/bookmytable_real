
from django.urls import path
from . import views



urlpatterns = [
    # Landing page: Are you a Customer or Owner?
    path('', views.select_user_type, name='select_user_type'),
    
    # Redirect to login or signup based on user type
    path('<str:user_type>/select-action/', views.select_action, name='select_action'),

    # Signup routes
    path('<str:user_type>/signup/', views.signup, name='signup'),

    # Login routes
    path('<str:user_type>/login/', views.login_view, name='login'),
    
    path('home/', views.home, name='home'),

    path('dashboard/', views.owner_dashboard, name='owner_dashboard'), 

    path('profile/', views.profile, name='profile'),

    path('logout/', views.logout_view, name='logout'),

    path('my-reservations/', views.my_reservations, name='my_reservations'),

    path('my-review/', views.my_review, name='my_review'),

    path('delete_reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
]