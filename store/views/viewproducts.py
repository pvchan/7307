import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from store.models.products import Products
from store.models.category import Category
from store.models.user import CustomUser, UserRole
from django.middleware.csrf import rotate_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

@method_decorator(csrf_protect, name='dispatch')
class ViewProducts(View):
    def get(self, request):
        # Get user roles
        customer_id = request.session.get('customer')
        roles = []
        if customer_id:
            try:
                customer = CustomUser.objects.get(id=customer_id)
                user_roles = UserRole.objects.filter(user=customer)
                for user_role in user_roles:
                    role_name = user_role.role.name.lower()
                    roles.append(role_name)
                    # Check if the user has either the 'staff' or 'admin' role
                    if role_name == 'staff' or role_name == 'admin':
                        products = Products.get_all_products()
                        context = {
                            'products': products,
                            'roles': roles,  # Include roles in the context
                        }
                        return render(request, 'viewproducts.html', context)
            except CustomUser.DoesNotExist:
                pass

        # Redirect to login or other page if the user does not have the required role
        return render(request, 'login.html', {'error': 'You must be admin or staff !!'})

@method_decorator(csrf_protect, name='dispatch')
class EditProduct(View):
    def get(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        categories = Category.get_all_categories()
        reviews = json.loads(product.review)
        return render(request, 'editproduct.html', {'product': product, 'categories': categories, 'reviews': reviews})
    
    def post(self, request, product_id):
        rotate_token(request)
        product = get_object_or_404(Products, id=product_id)
        product.name = request.POST.get('name', product.name)
        product.price = request.POST.get('price', product.price)
        product.description = request.POST.get('description', product.description)
        product.category.name = request.POST.get('category', product.category.name)
        if request.FILES:
            product.image = request.FILES['image']
        product.save()
        return redirect('viewproducts') # assumes the name of the url pattern for ViewProducts is 'view_products'

@method_decorator(csrf_protect, name='dispatch')
class NewProduct(View):
    def get(self, request):
        categories = Category.get_all_categories()
        return render(request, 'newproduct.html', {'categories': categories})

    def post(self, request):
        rotate_token(request)
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        product = Products(name=name, price=price, description=description, category=category)
        if request.FILES:
            product.image = request.FILES['image']
        product.save()
        return redirect('viewproducts')
