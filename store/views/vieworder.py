from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from store.models.user import CustomUser, UserRole
from store.models.orders import Order
from django.middleware.csrf import rotate_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

@method_decorator(csrf_protect, name='dispatch')
class ViewOrders(View):
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
                        orders = Order.objects.all()
                        return render(request, 'vieworders.html', {'orders': orders, 'roles': roles})
            except CustomUser.DoesNotExist:
                pass

        # Redirect to login or other page if the user does not have the required role
        return render(request, 'login.html', {'error': 'You must be admin or staff !!'})

@method_decorator(csrf_protect, name='dispatch')
class EditOrder(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'editorder.html', {'order': order})

    def post(self, request, order_id):
        rotate_token(request)
        order = get_object_or_404(Order, id=order_id)
        status = request.POST.get('status')
        order.status = True if status == 'paid' else False
        order.save()
        return redirect('vieworders')  # Use the correct name 'orders' instead of 'vieworders'

