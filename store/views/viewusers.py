from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from store.models.user import CustomUser, UserRole, Role

class ViewUsers(View):
    def get(self, request):
        # Check if the logged-in user has the 'Admin' role
        customer_id = request.session.get('customer')
        if customer_id:
            try:
                customer = CustomUser.objects.get(id=customer_id)
                if UserRole.objects.filter(user=customer, role__name='Admin').exists():
                    roles = Role.objects.all()  # Fetch all roles
                    return render(request, 'viewusers.html', {'roles': roles})
            except CustomUser.DoesNotExist:
                pass
        
        # Redirect to login or other page if the user does not have the required role
        return render(request, 'login.html', {'error': 'You must be admin !!'})


class EditUser(View):
    def get(self, request, user_id):
        # Same check for 'Admin' role as in the 'ViewUsers' class
        customer_id = request.session.get('customer')
        if customer_id:
            try:
                customer = CustomUser.objects.get(id=customer_id)
                if UserRole.objects.filter(user=customer, role__name='Admin').exists():
                    user = get_object_or_404(CustomUser, id=user_id)
                    roles = Role.objects.all()
                    return render(request, 'edituser.html', {'user': user, 'roles': roles})
            except CustomUser.DoesNotExist:
                pass
        
        return render(request, 'login.html', {'error': 'You must be admin !!'})