from django.shortcuts import render 
import stripe
from django.views import View
from store.models.products import Products
from django.conf import settings
from store.models.user import CustomUser
from store.models.orders import Order

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
    
#@login_required
def checkout(request):
    if request.method == "POST":
        checkout = stripe.Charge.create(
            amount=100,
            currency="aud",
            description="Payment",
            source=request.POST['stripeToken']
        )

        if checkout['status'] == 'succeeded':
            customer_id = request.session.get('customer')
            customer = CustomUser.objects.get(id=customer_id)

            cart = request.session.get('cart')
            for product_id, quantity in cart.items():
                product = Products.objects.get(id=product_id)

                # Retrieve address and phone number from the POST data
                address = request.POST.get('address')
                phone = request.POST.get('phone')

                # create order
                order = Order(
                    product=product,
                    customer=customer,
                    user=customer,
                    quantity=quantity,
                    price=product.price,
                    address=address,
                    phone=phone,
                )
                order.placeOrder()

            # Clear cart
            request.session['cart'] = {}

    return render(request , 'checkout.html')

