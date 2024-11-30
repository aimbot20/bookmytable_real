from django.urls import path
from . import views

urlpatterns = [
    # URL for selecting the payment method (Card or Wallet)
    path('<int:R_ID>/<int:T_ID>/<int:reservation_id>/', views.payment_page, name='payment_page'),
    
    # URL for making the payment by card
    path('<int:R_ID>/<int:T_ID>/<int:reservation_id>/card/', views.payment_by_card, name='payment_by_card'),
    
    # URL for making the payment by wallet
    path('<int:R_ID>/<int:T_ID>/<int:reservation_id>/wallet/', views.payment_by_wallet, name='payment_by_wallet'),

    path('<int:R_ID>/<int:T_ID>/<int:reservation_id>/success', views.payment_success, name='payment_success')

    
]
