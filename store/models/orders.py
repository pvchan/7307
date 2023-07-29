# models/orders.py
from django.db import models
from .products import Products  # Correct import for Products model
import datetime

class Order(models.Model):
    product = models.ForeignKey('store.Products', on_delete=models.CASCADE)
    customer = models.ForeignKey('store.CustomUser', on_delete=models.CASCADE)
    user = models.ForeignKey('store.CustomUser', on_delete=models.CASCADE, related_name='orders_as_user')
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        from .user import CustomUser  # Import inside the method to avoid circular import
        return Order.objects.filter(customer=customer_id).order_by('-date')
