from django.shortcuts import render
from django.views import View
from store.models.products import Products

class SearchView(View):
    def get(self, request):
        products = Products.objects.all()
        return render(request, 'search.html', {'products': products})
