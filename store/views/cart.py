from django.shortcuts import render 
import stripe
from django.views import View
from store.models.products import Products
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_id(ids)
        print(products)
        return render(request , 'cart.html' , {'products' : products} )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLIC_KEY
        return context
    
def checkout(request):
    if request.method == "POST":
        checkout = stripe.Charge.create(
            amount=100,
            currency="aud",
            description="Payment",
            source=request.POST['stripeToken']
        )
    return render(request , 'checkout.html')