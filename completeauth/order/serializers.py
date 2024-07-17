from rest_framework import serializers
from .email_draft import email_draft_create
from accounts.utils import Util

from .models import Order, OrderItem
from Product.models import Product
from Product.serializers import ProductSerializer

class MyOrderItemSerializer(serializers.ModelSerializer):    
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "product",
            "quantity",
        )

class MyOrderSerializer(serializers.ModelSerializer):
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

class OrderItemSerializer(serializers.ModelSerializer):   
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = OrderItem
        fields = (
            "product",
            "quantity",
        )

class MyCartSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "first_name",
            "last_name",
            "address",
            "pincode",
            "city",
            "items",
        )

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        amt = 0

        items = ""

        for item_data in items_data:
            try:
                product = Product.objects.get(id=item_data['product'].id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {item_data['product']} does not exist")

            price = product.price
            name = product.name
            items = items + name + ", "
            quantity = item_data['quantity']
            amt += price * quantity

        items = items[0:-2]
        validated_data['amount'] = amt
        validated_data['user'] = user
        order = Order.objects.create(**validated_data)


        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        body = email_draft_create(validated_data['first_name']+' '+validated_data['last_name'], items, amt)

        data = {
            'subject': 'Order Confirmation - Your Order Is Being Processed 🛒',
            'body': body,
            'to_email': user.email
        }
        Util.send_email(data)

        return order
    