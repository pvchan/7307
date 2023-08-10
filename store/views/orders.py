from django.shortcuts import render, redirect
from store.models.orders import Order
from store.models.user import UserRole, CustomUser
from django.views import View

class OrderView(View):
    def get(self, request):
        customer_id = request.session.get('customer')
        roles = []
        is_customer = False
        if customer_id:
            try:
                customer = CustomUser.objects.get(id=customer_id)
                user_roles = UserRole.objects.filter(user=customer)
                for user_role in user_roles:
                    role_name = user_role.role.name.lower()
                    roles.append(role_name)
                    if role_name == 'customer':
                        is_customer = True
                        break
            except CustomUser.DoesNotExist:
                pass

        if is_customer:
            orders = Order.objects.filter(customer=customer).order_by('-date')
            return render(request, 'orders.html', {'orders': orders, 'roles': roles})
        else:
            return render(request, 'login.html', {'error': 'You must be a customer to access your orders!'})
