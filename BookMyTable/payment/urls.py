from django.urls import path
from . import views

urlpatterns = [

    path('<int:R_ID>/<int:T_ID>/<int:reservation_id>/', views.payment_page, name='payment_page'),

    path('<int:R_ID>/<int:T_ID>/<int:reservation_id>/card/', views.payment_by_card, name='payment_by_card'),
    
    path('<int:R_ID>/<int:T_ID>/<int:reservation_id>/wallet/', views.payment_by_wallet, name='payment_by_wallet'),

    path('<int:R_ID>/<int:T_ID>/<int:reservation_id>/success', views.payment_success, name='payment_success')

]
