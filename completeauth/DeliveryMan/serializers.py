from rest_framework import serializers
from .models import DeliveryMan
from order.models import Order
from order.serializers import MyOrderItemSerializer

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
            "delivered_status",
            "items",
        )