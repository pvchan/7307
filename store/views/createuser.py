from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.user import CustomUser
from django.views import View
from store.models.user import CustomUser, UserRole, Role

class CreateUser(View):
    def get(self, request):
        return render(request, 'createuser.html')

    def post(self, request):
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = CustomUser(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=make_password(password),
            is_staff=True if user_type == 'STAFF' else False,
            is_admin=True if user_type == 'ADMIN' else False,
        )
        user.save()

        role = Role.objects.get(name=user_type)

        user_role = UserRole(user=user, role=role)
        user_role.save()

        return redirect('admin_dashboard')  # or wherever you want to redirect after creating a user
