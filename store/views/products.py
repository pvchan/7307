import json
from django.shortcuts import render, redirect
from django.views import View
from store.models.products import Products
from store.models.category import Category
from store.models.user import CustomUser
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self, request, product_id):
        product = Products.objects.get(id=product_id)
        review = json.loads(product.review)
        return render(request, 'products.html', {'product' : product, 'reviews': review})
    
    def post(self, request, product_id):
        product_name = request.POST.get('product')
        customer_id = request.POST.get('customer')
        review_text = request.POST.get('review')

        # fetch the customer's name
        customer = CustomUser.objects.get(id=customer_id)
        customer_name = customer.first_name + " " + customer.last_name

        product_db = Products.objects.get(id=product_id)

        # Create a dictionary for the new review
        new_review = {"customer_name": customer_name, "review": review_text}

        if product_db.review == '{}':
            # If there are no existing reviews, create a new list with the new review
            reviews = [new_review]
        else:
            # If there are existing reviews, append the new review to the list
            reviews = json.loads(product_db.review)
            reviews.append(new_review)

        # Convert the list of reviews back to a string and update the product in the database
        Products.objects.filter(id=product_id).update(review=json.dumps(reviews))

        return redirect(f'/product/{product_id}')

