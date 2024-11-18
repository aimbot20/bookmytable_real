
from django.contrib import admin
from .models import Payment, PaymentByCard, PaymentByWallet, Card, Wallet, PaymentDate, PaymentWithDate

# Admin class for Payment
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'amount', 'status', 'reservation')
    search_fields = ('payment_id', 'reservation__id')  # Allow searching by reservation id
    list_filter = ('status',)  # Filter payments by their status

# Admin class for PaymentByCard
class PaymentByCardAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'card', 'amount', 'status', 'reservation')
    search_fields = ('payment_id', 'card__card_number')  # Search by card number
    list_filter = ('status',)

# Admin class for PaymentByWallet
class PaymentByWalletAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'wallet', 'amount_in_wallet', 'status', 'reservation')
    search_fields = ('payment_id', 'wallet__user__username')  # Search by user associated with the wallet
    list_filter = ('status',)

#Admin class for Card
class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'expiry_date', 'cardholder_name')
    search_fields = ('card_number', 'user__username')  # Search by card number or user
    fields = ('user', 'card_number', 'expiry_date', 'cardholder_name')

# Admin class for Wallet
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)

# Admin class for PaymentDate
class PaymentDateAdmin(admin.ModelAdmin):
    list_display = ('payment', 'date')
    search_fields = ('payment__payment_id',)

# Admin class for PaymentWithDate
class PaymentWithDateAdmin(admin.ModelAdmin):
    list_display = ('payment', 'payment_date')
    search_fields = ('payment__payment_id',)

# Register the models with the Django admin
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentByCard, PaymentByCardAdmin)
admin.site.register(PaymentByWallet, PaymentByWalletAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(PaymentDate, PaymentDateAdmin)
admin.site.register(PaymentWithDate, PaymentWithDateAdmin)
