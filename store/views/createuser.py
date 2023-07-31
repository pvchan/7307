from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from store.models.user import CustomUser, UserRole, Role
from django.views import View

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

        # Validate the email address
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError as e:
            error_message = e.messages[0]
            data = {
                'error': error_message,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'user_type': user_type,
            }
            return render(request, 'createuser.html', data)

        # Check if a user with the same email already exists
        if CustomUser.objects.filter(email=email).exists():
            error_message = 'A user with the same email already exists.'
            data = {
                'error': error_message,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'user_type': user_type,
            }
            return render(request, 'createuser.html', data)

        user = CustomUser(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=make_password(password),
            is_staff=user_type == 'STAFF',
            is_admin=user_type == 'ADMIN',
        )
        user.save()

        role_name = user_type.title()
        role = Role.objects.get(name=role_name)

        user_role = UserRole(user=user, role=role)
        user_role.save()

        return redirect('admin_dashboard') 
