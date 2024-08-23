from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from order.permissions import IsNotDeliveryMan
from .serializers import UserProfileSerializer, DeliveryOrderSerializer
from .models import DeliveryMan
from order.models import Order, OrderItem

# Create your views here.
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated, IsNotDeliveryMan]

    def get(self, request, format=None):
        delivery_man = DeliveryMan.objects.filter(user = request.user)
        print(delivery_man)
        serializer = UserProfileSerializer(delivery_man, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AllOrdersDelivery(APIView):
    permission_classes = [IsAuthenticated, IsNotDeliveryMan]

    def get(self, request, format=None):
        delivery_man_var = DeliveryMan.objects.get(user = request.user)
        orders = Order.objects.filter(delivery_man=delivery_man_var)
        serializer = DeliveryOrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrdersDelivery(APIView):
    permission_classes = [IsAuthenticated, IsNotDeliveryMan]

    def get(self, request, format=None):
        delivery_man_var = DeliveryMan.objects.get(user = request.user)
        orders = Order.objects.filter(delivery_man=delivery_man_var, delivered_status=False)
        serializer = DeliveryOrderSerializer(orders, many=True)
        return Response(serializer.data)


