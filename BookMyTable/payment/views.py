from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Payment, PaymentByCard, PaymentByWallet, Card
from reservation.models import Reservation
from django.contrib.auth.decorators import login_required

# im using a standard cost for all reservations rn 
STANDARD_RESERVATION_COST = 50  

# View to display payment options (Card or Wallet)
@login_required
def payment_page(request,  R_ID, T_ID, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # Ensure the reservation belongs to the logged-in user
    if reservation.customer != request.user:
        return HttpResponse("You are not authorized to make payment for this reservation.")

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        if payment_method == "card":
            return redirect('payment_by_card', R_ID=R_ID, T_ID=T_ID, reservation_id=reservation.id)
        elif payment_method == "wallet":
            return redirect("payment_by_wallet",R_ID=R_ID, T_ID=T_ID, reservation_id=reservation.id)

    return render(request, "payment/payment_page.html", {"reservation": reservation})

# View to process payment via card
@login_required
def payment_by_card(request, R_ID, T_ID, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    reservation_cost = STANDARD_RESERVATION_COST


    # Ensure the reservation belongs to the logged-in user
    if reservation.customer != request.user:
        return HttpResponse("You are not authorized to make payment for this reservation.")

    user_cards = Card.objects.filter(customer=request.user)

    if request.method == "POST":
        card_option = request.POST.get("card_option")

        if card_option == "existing_card":
            card_id = request.POST.get("card_id")
            card = get_object_or_404(Card, id=card_id, customer=request.user)
            amount = reservation_cost

            payment = PaymentByCard.objects.create(
                amount=amount,
                reservation=reservation,
                saved_card=card,
                status="Completed"
            )
            payment.confirm_payment()
            return redirect("payment_success",R_ID=R_ID, T_ID=T_ID, reservation_id=reservation.id )

        elif card_option == "new_card":
            card_number = request.POST.get("new_card_number")
            expiry_date = request.POST.get("new_card_expiry")
            cardholder_name = request.POST.get("new_card_holder")

            if not all([card_number, expiry_date, cardholder_name]):
                return HttpResponse("All fields are required for adding a new card.")

            new_card = Card.objects.create(
                customer=request.user,
                card_number=card_number,
                expiry_date=expiry_date,
                cardholder_name=cardholder_name
            )

            amount = reservation_cost
            payment = PaymentByCard.objects.create(
                amount=amount,
                reservation=reservation,
                card_number=card_number,
                expiry_date=expiry_date,
                cardholder_name=cardholder_name,
                status="Completed"
            )
            payment.confirm_payment()
            return redirect("payment_success", R_ID=R_ID, T_ID=T_ID, reservation_id=reservation.id)

    return render(request, "payment/payment_by_card.html", {
        "reservation": reservation,
        "user_cards": user_cards
    })

# View to process payment via wallet
@login_required
def payment_by_wallet(request,  R_ID, T_ID, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation_cost = STANDARD_RESERVATION_COST

    # Ensure the reservation belongs to the logged-in user
    if reservation.customer != request.user:
        return HttpResponse("You are not authorized to make payment for this reservation.")

    if request.method == "POST":
        amount = reservation_cost

        # Deduct amount from wallet
        if request.user.deduct_from_wallet(amount):
            payment = PaymentByWallet.objects.create(
                amount=amount,
                reservation=reservation,
                status="Completed"
            )
            payment.confirm_payment()
            return redirect("payment_success", R_ID=R_ID, T_ID=T_ID, reservation_id=reservation.id)
        else:
            return HttpResponse("Insufficient funds in your wallet.")

    return render(request, "payment/payment_by_wallet.html", {"reservation": reservation})


@login_required
def payment_success(request, R_ID, T_ID, reservation_id):
    # Fetch the reservation object
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # Get the latest payment associated with the reservation
    payment = get_object_or_404(Payment, reservation=reservation)

    # Update the table's is_reserved field to True when payment is successful
    table = reservation.table
    table.is_reserved = True
    table.save()  # Save the updated table object

    # Update the reservation's status to "Confirmed"
    reservation.reservation_status = "Confirmed"
    reservation.save()  # Save the updated reservation object

    return render(request, "payment/payment_success.html", {
        "payment": payment,
        "reservation_id": reservation_id,
        "R_ID": R_ID,
        "T_ID": T_ID
    })