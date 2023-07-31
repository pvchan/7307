from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.user import CustomUser, Role, UserRole
from django.views import View

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        username = postData.get('username')
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone_number = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        # Validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            'email': email
        }
        error_message = None

        user = CustomUser(username=username, first_name=first_name, last_name=last_name, phone_number=phone_number, email=email, password=password)
        error_message = self.validateUser(user)

        if not error_message:
            user.password = make_password(user.password)
            user.save()

            # Assign 'customer' role to the user
            customer_role, _ = Role.objects.get_or_create(name='customer', description='Customer Role')
            UserRole.objects.create(user=user, role=customer_role)

            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)
        
        
    def validateUser(self, user):
        error_message = None
        if (not user.first_name):
            error_message = "Please Enter your First Name !!"
        elif len(user.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not user.last_name:
            error_message = 'Please Enter your Last Name'
        elif len(user.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif CustomUser.objects.filter(username=user.username).exists():
            error_message = 'Username Already Registered..'
        elif not user.phone_number:
            error_message = 'Enter your Phone Number'
        elif len(user.phone_number) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(user.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len(user.email) < 5:
            error_message = 'Email must be 5 char long'
        elif CustomUser.objects.filter(email=user.email).exists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message

