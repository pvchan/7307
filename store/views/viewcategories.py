from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from store.models.category import Category

class ViewCategories(View):
    def get(self, request):
        categories = Category.get_all_categories()
        return render(request, 'viewcategories.html', {'categories': categories})

class EditCategory(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        return render(request, 'editcategory.html', {'category': category})

    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category.name = request.POST.get('name', category.name)
        category.save()
        return redirect('viewcategories') # assumes the name of the url pattern for ViewCategories is 'view_categories'

class NewCategory(View):
    def get(self, request):
        return render(request, 'newcategory.html')

    def post(self, request):
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
        return redirect('viewcategories')  # redirect to the category list after a new category is created
