import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from store.models.products import Products
from store.models.category import Category

class ViewProducts(View):
    def get(self, request):
        products = Products.get_all_products()
        return render(request, 'viewproducts.html', {'products': products})

class EditProduct(View):
    def get(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        categories = Category.get_all_categories()
        reviews = json.loads(product.review)
        return render(request, 'editproduct.html', {'product': product, 'categories': categories, 'reviews': reviews})
    
    def post(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        product.name = request.POST.get('name', product.name)
        product.price = request.POST.get('price', product.price)
        product.description = request.POST.get('description', product.description)
        product.category.name = request.POST.get('category', product.category.name)
        if request.FILES:
            product.image = request.FILES['image']
        product.save()
        return redirect('viewproducts') # assumes the name of the url pattern for ViewProducts is 'view_products'

class NewProduct(View):
    def get(self, request):
        categories = Category.get_all_categories()
        return render(request, 'newproduct.html', {'categories': categories})

    def post(self, request):
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
