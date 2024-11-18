from django.db import models
from django.conf import settings  # To refer to the custom user model
from datetime import datetime

# Payment Status Enum 
class PaymentStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    COMPLETED = 'Completed', 'Completed'
   

# Date class (stores payment date)
class PaymentDate(models.Model):
    payment = models.OneToOneField('Payment', on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)  # Store the date of payment

    def __str__(self):
        return f"Payment Date: {self.date}"

# Card model to store card details
class Card(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)  
    expiry_date = models.DateField()
    cardholder_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Card ending with {self.card_number[-4:]}"  # Display last 4 digits

# Wallet model to store user wallet balance
class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)  # Money in wallet

    def __str__(self):
        return f"Wallet balance for {self.user.username}: {self.balance}"

# Base Payment model
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    reservation = models.ForeignKey('reservation.Reservation', on_delete=models.CASCADE)  # Link to reservation

    def __str__(self):
        return f"Payment {self.payment_id} for reservation {self.reservation.id}"

    def confirm_payment(self):
        # Logic to confirm the payment based on the payment type (card or wallet)
        pass

    def get_payment_done(self, cust_id: int, amount: float):
        # Logic to complete the payment process
        pass

# Payment made via Card (child class of Payment)
class PaymentByCard(Payment):
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, blank=True)  # Card used for the payment

    def __str__(self):
        return f"Payment {self.payment_id} by Card"

# Payment made via Wallet (child class of Payment)
class PaymentByWallet(Payment):
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, blank=True)  # Wallet used for the payment
    amount_in_wallet = models.FloatField()

    def __str__(self):
        return f"Payment {self.payment_id} by Wallet"

    def confirm_payment(self):
        if self.wallet.balance >= self.amount:  # Check if enough balance is available
            self.wallet.balance -= self.amount  # Deduct from wallet balance
            self.wallet.save()
            self.status = PaymentStatus.COMPLETED
            self.save()
        else:
            self.status = PaymentStatus.FAILED
            self.save()

# Optionally, you can add the PaymentDate model to connect the payment to a date
class PaymentWithDate(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    payment_date = models.OneToOneField(PaymentDate, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment {self.payment_id} on {self.payment_date.date}"
