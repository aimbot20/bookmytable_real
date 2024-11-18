from django.urls import path
from . import views

urlpatterns = [
    path('<int:R_ID>/<int:T_ID>/details/', views.reservation_details, name='reservation_details'),
]
