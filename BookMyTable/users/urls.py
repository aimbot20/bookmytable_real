
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
]