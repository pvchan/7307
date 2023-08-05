from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from store.models.category import Category
from store.models.user import CustomUser, UserRole

class ViewCategories(View):
    def get(self, request):
        customer_id = request.session.get('customer')
        roles = []
        if customer_id:
            try:
                customer = CustomUser.objects.get(id=customer_id)
                user_roles = UserRole.objects.filter(user=customer)
                for user_role in user_roles:
                    role_name = user_role.role.name.lower()
                    roles.append(role_name)
                    if role_name == 'admin':
                        categories = Category.get_all_categories()
                        return render(request, 'viewcategories.html', {'categories': categories, 'roles': roles})
            except CustomUser.DoesNotExist:
                pass
        return render(request, 'login.html', {'error': 'You must be admin !!'})

class EditCategory(View):
    def get(self, request, category_id):
        customer_id = request.session.get('customer')
        roles = []
        if customer_id:
            try:
                customer = CustomUser.objects.get(id=customer_id)
                user_roles = UserRole.objects.filter(user=customer)
                for user_role in user_roles:
                    role_name = user_role.role.name.lower()
                    roles.append(role_name)
                    if role_name == 'admin':
                        category = get_object_or_404(Category, id=category_id)
                        return render(request, 'editcategory.html', {'category': category, 'roles': roles})
            except CustomUser.DoesNotExist:
                pass
        return render(request, 'login.html', {'error': 'You must be admin !!'})

    def post(self, request, category_id):
        # The post method should also be restricted to admin users
        customer_id = request.session.get('customer')
        if customer_id:
            try:
                customer = CustomUser.objects.get(id=customer_id)
                user_roles = UserRole.objects.filter(user=customer)
                for user_role in user_roles:
                    if user_role.role.name.lower() == 'admin':
                        category = get_object_or_404(Category, id=category_id)
                        category.name = request.POST.get('name', category.name)
                        category.save()
                        return redirect('viewcategories')
            except CustomUser.DoesNotExist:
                pass
        return render(request, 'login.html', {'error': 'You must be admin !!'})

class NewCategory(View):
    def get(self, request):
        customer_id = request.session.get('customer')
        roles = []
        if customer_id:
            try:
                customer = CustomUser.objects.get(id=customer_id)
                user_roles = UserRole.objects.filter(user=customer)
                for user_role in user_roles:
                    role_name = user_role.role.name.lower()
                    roles.append(role_name)
                    if role_name == 'admin':
                        return render(request, 'newcategory.html', {'roles': roles})
            except CustomUser.DoesNotExist:
                pass
        return render(request, 'login.html', {'error': 'You must be admin !!'})

    def post(self, request):
        # The post method should also be restricted to admin users
        customer_id = request.session.get('customer')
        if customer_id:
            try:
                customer = CustomUser.objects.get(id=customer_id)
                user_roles = UserRole.objects.filter(user=customer)
                for user_role in user_roles:
                    if user_role.role.name.lower() == 'admin':
                        name = request.POST.get('name')
                        if name:
                            Category.objects.create(name=name)
                        return redirect('viewcategories')
            except CustomUser.DoesNotExist:
                pass
        return render(request, 'login.html', {'error': 'You must be admin !!'})