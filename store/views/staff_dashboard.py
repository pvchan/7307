from django.shortcuts import render
from django.views import View
from store.models.user import CustomUser, UserRole

class StaffView(View):
    def get(self, request):
        # Get user roles
        customer_id = request.session.get('customer')
        roles = []
        if customer_id:
            try:
                customer = CustomUser.objects.get(id=customer_id)
                user_roles = UserRole.objects.filter(user=customer)
                for user_role in user_roles:
                    role_name = user_role.role.name.lower()
                    roles.append(role_name)
                    # Check if the user has either the 'staff' or 'admin' role
                    if role_name == 'staff' or role_name == 'admin':
                        context = {
                            'roles': roles,  # Include roles in the context
                        }
                        return render(request, 'staff_dashboard.html', context)
            except CustomUser.DoesNotExist:
                pass

        # Redirect to login or other page if the user does not have the required role
        return render(request, 'login.html', {'error': 'You must be admin or staff !!'})