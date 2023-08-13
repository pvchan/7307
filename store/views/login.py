from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from store.models.user import CustomUser, UserRole
from django.views import View
from django.middleware.csrf import rotate_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

@method_decorator(csrf_protect, name='dispatch')
class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('next')
        return render(request, 'login.html')

    def post(self, request):
        rotate_token(request)
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            customer = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            customer = None
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                user_roles = UserRole.objects.filter(user=customer)
                for user_role in user_roles:
                    role_name = user_role.role.name.lower()
                    if role_name == 'admin':
                        return redirect('admin_dashboard')
                    elif role_name == 'staff':
                        return redirect('staff_dashboard')
                
                # Redirect to the return_url or homepage if the user has no specific role
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')
