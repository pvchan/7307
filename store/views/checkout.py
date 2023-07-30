# checkout.py
import json
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from store.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

def calculate_total_amount(order):
    total_amount = 0
    for item in order.items.all():
        total_amount += item.product.price * item.quantity
    return total_amount

class CreatePaymentIntentView(View):
    def post(self, request):
        try:
            # Fetch order by ID or create a new one
            order = Order.objects.get(id=request.POST.get('order_id'))  # replace with your own function

            # Calculate total amount of the order
            total_amount = calculate_total_amount(order)  # replace with your own function

            # Create a PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=total_amount,  # amount is in cents
                currency='usd',
            )

            # Save the PaymentIntent ID to the order
            order.payment_intent_id = intent.id
            order.save()

            # Send the client secret to the front end
            return JsonResponse({'clientSecret': intent.client_secret})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
