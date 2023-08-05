from django.shortcuts import render
from django.views import View
from store.models.user import CustomUser, UserRole

class AdminView(View):
    def get(self, request):
        # Get the customer ID from the session
        customer_id = request.session.get('customer')

        # If the customer ID is found, retrieve the CustomUser object
        if customer_id:
            try:
                customer = CustomUser.objects.get(id=customer_id)
                # Check if the user has the admin role
                user_roles = UserRole.objects.filter(user=customer)
                roles = []
                for user_role in user_roles:
                    role_name = user_role.role.name.lower()
                    roles.append(role_name)
                    if role_name == 'admin':
                        return render(request, 'admin_dashboard.html', {'roles': roles})
            except CustomUser.DoesNotExist:
                pass
        
        # Redirect to login or other page if the user is not an admin
        return render(request, 'login.html', {'error': 'You must be admin !!'})