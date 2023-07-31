from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from store.models.orders import Order

class ViewOrders(View):
    def get(self, request):
        orders = Order.objects.all()
        return render(request, 'vieworders.html', {'orders': orders})

class EditOrder(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'editorder.html', {'order': order})

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        status = request.POST.get('status')
        order.status = True if status == 'paid' else False
        order.save()
        return redirect('vieworders')  # Use the correct name 'orders' instead of 'vieworders'

