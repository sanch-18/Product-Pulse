from rest_framework import serializers
from .models import DeliveryMan
from order.models import Order, OrderItem
from order.serializers import MyOrderItemSerializer
from Product.models import Product
from Product.serializers import ProductSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMan
        fields = [
            'id',
            'email',
            'phone',
            'name',
            'city',
            'location',
            'pincode', 
            'salary'
        ]

class MyOrderItemSerializer(serializers.ModelSerializer):    
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "product",
            "quantity",
        )

class DeliveryOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "address",
            "pincode",
            "city",
            "amount",
            "created_at",
            "delivery_date",
            "delivered_status",
            "items",
        )