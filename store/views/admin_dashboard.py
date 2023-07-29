from django.shortcuts import render, redirect
from django.views import View
from store.models.products import Products
from store.models.category import Category
from store.models.user import CustomUser

class AdminView(View):
    def get(self, request):
        return render(request, 'admin_dashboard.html')