from django.contrib import admin
from .models import Payment, PaymentByCard, PaymentByWallet, Card

# Admin class for Payment
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'amount', 'status', 'reservation', 'payment_date')
    search_fields = ('payment_id', 'reservation__id')  # Allow searching by reservation id
    list_filter = ('status',)  # Filter payments by their status

# Admin class for PaymentByCard
class PaymentByCardAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'saved_card', 'card_number', 'amount', 'status', 'reservation')
    search_fields = ('payment_id', 'saved_card__card_number', 'card_number')  # Search by saved or one-time card number
    list_filter = ('status',)

    def card_number_display(self, obj):
        if obj.saved_card:
            return f"Saved Card: {obj.saved_card.card_number[-4:]}"
        return f"One-Time Card: {obj.card_number[-4:] if obj.card_number else 'N/A'}"

# Admin class for PaymentByWallet
class PaymentByWalletAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'amount', 'status', 'reservation')
    search_fields = ('payment_id', 'reservation__customer__username')  # Search by customer username
    list_filter = ('status',)

# Admin class for Card
class CardAdmin(admin.ModelAdmin):
    list_display = ('customer', 'card_number', 'expiry_date', 'cardholder_name')
    search_fields = ('card_number', 'customer__username')  # Search by card number or customer username
    fields = ('customer', 'card_number', 'expiry_date', 'cardholder_name')  # Fields displayed when editing



admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentByCard, PaymentByCardAdmin)
admin.site.register(PaymentByWallet, PaymentByWalletAdmin)
admin.site.register(Card, CardAdmin)
