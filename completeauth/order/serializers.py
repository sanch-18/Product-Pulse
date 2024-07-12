from rest_framework import serializers

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

        for item_data in items_data:
            try:
                product = Product.objects.get(id=item_data['product'].id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {item_data['product']} does not exist")

            price = product.price
            quantity = item_data['quantity']
            amt += price * quantity

        validated_data['amount'] = amt
        validated_data['user'] = user
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            
        return order
    
class DeleteOrderSerializer(serializers.Serializer):
    class Meta:
        model = Order
        fields = (
            "id",
        )