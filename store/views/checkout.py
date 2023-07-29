from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.user import CustomUser
from django.views import View
from store.models.products import Products
from store.models.orders import Order

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer_id = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        print(address, phone, customer_id, cart, products)

        # Fetch the actual Customer object from the database
        customer = CustomUser.objects.get(id=customer_id)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=customer,
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('cart')
