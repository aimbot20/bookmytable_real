from django.db import models
from django.conf import settings
from datetime import datetime
from users.models import Users, Customer


# PAYMENT STATUS - Enumerated class 
class PaymentStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    COMPLETED = 'Completed', 'Completed'


# CARD CLASS - to hold card info
class Card(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,                    # Link to the custom User model (Customer)
        on_delete=models.CASCADE,
        limit_choices_to={'is_customer': True},      # Ensure only customers can save cards
        related_name="saved_cards"  # Allows reverse access (customer.saved_cards)
    )
    card_number = models.CharField(max_length=16)  
    expiry_date = models.DateField()
    cardholder_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Card ending with {self.card_number[-4:]}"


# PAYMENT - parent class
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    reservation = models.ForeignKey('reservation.Reservation', on_delete=models.CASCADE)  # Link to reservation
    payment_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Payment {self.payment_id} for Reservation {self.reservation.id}"

    def confirm_payment(self):
        self.status = PaymentStatus.COMPLETED
        self.save()


# PAYMENT BY CARD - child of Payment
class PaymentByCard(Payment):
    saved_card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, blank=True)  # Use a saved card
    card_number = models.CharField(max_length=16, blank=True, null=True)  # For one-time card use
    expiry_date = models.DateField(blank=True, null=True)
    cardholder_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        if self.saved_card:
            return f"Payment done by Saved Card ending at {self.saved_card.card_number[-4:]}"
        return f"Payment done by One-Time Card ending {self.card_number[-4:]}"


# PAYMENT BY WALLET - child of Payment
class PaymentByWallet(Payment):
    def confirm_payment(self):
        customer = self.reservation.customer
        if customer.deduct_from_wallet(self.amount):  # Deduct from the customer's wallet
            self.status = PaymentStatus.COMPLETED
        else:
            self.status = PaymentStatus.PENDING  # Or Failed if you want a new status
        self.save()

    def __str__(self):
        return f"Payment {self.payment_id} by Wallet"
