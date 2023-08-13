from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from store.models.user import CustomUser, UserRole, Role
from django.views import View
from django.utils.decorators import method_decorator
from django.middleware.csrf import rotate_token
from django.views.decorators.csrf import csrf_protect

@method_decorator(csrf_protect, name='dispatch')
class CreateUser(View):
    def get(self, request):
        # Check if the logged-in user has the 'Admin' role
        customer_id = request.session.get('customer')
        roles = []
        if customer_id:
            try:
                customer = CustomUser.objects.get(id=customer_id)
                if UserRole.objects.filter(user=customer, role__name='Admin').exists():
                    user_roles = UserRole.objects.filter(user=customer)
                    for user_role in user_roles:
                        role_name = user_role.role.name.lower()
                        roles.append(role_name)
                    return render(request, 'createuser.html', {'roles': roles})
            except CustomUser.DoesNotExist:
                pass
        
        # Redirect to login or other page if the user does not have the required role
        return render(request, 'login.html', {'error': 'You must be admin !!'})

    def post(self, request):
        rotate_token(request)
        # Same check for 'Admin' role as in the 'get' method
        customer_id = request.session.get('customer')
        if not customer_id or not UserRole.objects.filter(user__id=customer_id, role__name='Admin').exists():
            return render(request, 'login.html', {'error': 'You must be admin !!'})

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
