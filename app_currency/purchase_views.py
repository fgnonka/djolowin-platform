import stripe

from django.db import models
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from wallet.models import UserWallet
from account.models import CustomUser
from .models import CurrencyPackage
from transaction.utils import create_currency_purchase_transaction



@login_required
def purchase_currency_package(request, package_id):
    currency_package = get_object_or_404(CurrencyPackage, id=package_id)

    if request.method == "POST":
        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            customer_email=request.user.email,
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": settings.DEFAULT_CURRENCY,  # Set your desired currency
                        "unit_amount": int(
                            currency_package.price * 100
                        ),  # Convert the price to cents
                        "product_data": {
                            "name": currency_package.name,
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("currency:purchase_success"))
            + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("currency:purchase_cancel")),
        )

        return redirect(session.url, code=303)
    else:
        context = {
            "currency_package": currency_package,
            "stripe_public_key": settings.STRIPE_PUBLISHABLE_KEY,
        }
        return render(request, "djolowin/app_currency/purchase_currency.html", context)


def purchase_success(request):
    user = request.user
    wallet = get_object_or_404(UserWallet, user=user)
    balance = wallet.balance
    context = {
        "balance": balance,
    }
    # Process the successful payment, update the user's Wallet, etc.
    return render(request, "djolowin/app_currency/purchase_success.html", context)


def purchase_cancel(request):
    return render(request, "djolowin/app_currency/purchase_cancel.html")


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponseBadRequest()
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponseBadRequest()
    else:
        # Handle the checkout.session.completed event
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            # ...
            print(session)
        # Get the user and currency package from the session (you may need to adjust this based on your implementation)
            session_user = CustomUser.objects.get(email=session["customer_email"])
            currency_package = CurrencyPackage.objects.get(
            price=session["amount_total"] / 100
        )
        #Record the purchase in your database
            transaction = create_currency_purchase_transaction(
            user = session_user, 
            currency_package = currency_package,
            amount_spent = int(session["amount_total"] / 100),
            
        )

            # Update the user's Wallet balance
            UserWallet.objects.filter(user=session_user).update(
                balance=models.F("balance") + currency_package.in_app_currency
            )

            # Perform any other actions required for a successful purchase

        return HttpResponse(status=200)