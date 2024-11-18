

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Payment, PaymentByCard, PaymentByWallet, Card, Wallet
from reservation.models import Reservation
from django.contrib.auth.decorators import login_required


# View to display payment options (Card or Wallet)
@login_required
def payment_page(request,  R_ID, T_ID, reservation_id):
    # Get the reservation object based on reservation_id
    reservation = Reservation.objects.get(id=reservation_id)

    # Ensure the reservation belongs to the logged-in user
    if reservation.customer != request.user:
        return HttpResponse("You are not authorized to make payment for this reservation.")

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")

        if payment_method == "card":
            # Handle card payment option
            return redirect("payment_by_card", reservation_id=reservation.id)

        elif payment_method == "wallet":
            # Handle wallet payment option
            return redirect("payment_by_wallet", reservation_id=reservation.id)
        
    return render(request, "payment/payment_page.html", {"reservation": reservation})

# View to process payment via card
@login_required
def payment_by_card(request, R_ID, T_ID, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)

    if reservation.customer != request.user:
        return HttpResponse("You are not authorized to make payment for this reservation.")
    

    print(f"User: {request.user}")


    # Initialize user_cards for both GET and POST requests
    user_cards = Card.objects.filter(user=request.user)

    if request.method == "POST":
        card_option = request.POST.get("card_option")
        
        if card_option == "existing_card":
            card_id = request.POST.get("card_id")
            card = Card.objects.get(id=card_id)
            amount = reservation.restaurant.reservation_cost  # Example, use actual logic for the amount
            payment = PaymentByCard.objects.create(
                amount=amount,
                reservation=reservation,
                card=card,
                status="Completed"
            )
            # Confirm payment here
            payment.confirm_payment()
            return redirect("payment_success", payment_id=payment.id)

        elif card_option == "new_card":
            # Add new card
            card_number = request.POST.get("card_number")
            expiry_date = request.POST.get("expiry_date")
            cardholder_name = request.POST.get("cardholder_name")
            if not card_number or not expiry_date or not cardholder_name:
                return HttpResponse("All fields are required for adding a new card.")

            new_card = Card.objects.create(
                user=request.user,
                card_number=card_number,
                expiry_date=expiry_date,
                cardholder_name=cardholder_name
            )
            # Create a new payment using this card
            amount = reservation.restaurant.reservation_cost
            payment = PaymentByCard.objects.create(
                amount=amount,
                reservation=reservation,
                card=new_card,
                status="Completed"
            )
            # Confirm payment
            payment.confirm_payment()
            return redirect("payment_success", payment_id=payment.id)

    # Render the page with the user cards and reservation info
    return render(request, "payment/payment_by_card.html", {
        "reservation": reservation,
        "user_cards": user_cards
    })

# View to process payment via wallet
@login_required
def payment_by_wallet(request,  R_ID, T_ID, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)

    if reservation.customer != request.user:
        return HttpResponse("You are not authorized to make payment for this reservation.")
    
    if request.method == "POST":
        # Get the user's wallet
        wallet = Wallet.objects.get(user=request.user)
        amount = reservation.restaurant.reservation_cost
        
        # Check if the user has enough balance
        if wallet.balance >= amount:
            payment = PaymentByWallet.objects.create(
                amount=amount,
                reservation=reservation,
                wallet=wallet,
                amount_in_wallet=wallet.balance,
                status="Completed"
            )
            # Confirm wallet payment
            payment.confirm_payment()
            return redirect("payment_success", payment_id=payment.id)
        else:
            return HttpResponse("Insufficient funds in your wallet.")
    
    return render(request, "payment/payment_by_wallet.html", {"reservation": reservation})

# View for successful payment
@login_required
def payment_success(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    return render(request, "payment/payment_success.html", {"payment": payment})
