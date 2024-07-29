from django.db import models
from Product.models import Product
from accounts.models import User
from DeliveryMan.models import DeliveryMan 

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders',blank=True, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_status = models.BooleanField(default=False)
    delivery_date = models.DateField(blank=True, null=True)
    preferred_date = models.DateField(blank=True, null=True)
    is_processed = models.BooleanField(default=False)
    delivery_man = models.ForeignKey(DeliveryMan, related_name='delivery',blank=True, null=True, on_delete=models.SET_NULL)

    class meta:
        ordering = ['created_at', ]
    
    def __str__(self):
        return str(self.is_processed) + ' - '+ self.pincode
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="items", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s'%self.id
    