from django.shortcuts import render, redirect
from django.views import View
from store.models.products import Products
from store.models.category import Category
from store.models.user import CustomUser

class StaffView(View):
    def get(self, request):
        return render(request, 'staff_dashboard.html')