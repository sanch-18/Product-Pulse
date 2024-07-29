from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import MyOrderSerializer, MyCartSerializer
from .models import Order
from rest_framework import serializers
from django.utils import timezone
from accounts.utils import Util
from .email_draft import email_draft_delete
from .permissions import IsDeliveryman

class OrdersList(APIView):
    permission_classes = [IsAuthenticated, IsDeliveryman]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderCart(APIView):
    permission_classes = [IsAuthenticated, IsDeliveryman]

    def post(self, request):
        serializer = MyCartSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            try:
                order = serializer.save()
                
                return Response({
                    'msg': 'Your Order has been placed'
                }, status=status.HTTP_200_OK)
            except serializers.ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCart(APIView):
    permission_classes = [IsAuthenticated, IsDeliveryman]

    def delete(self, request):
        order_id = request.data.get('id')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'msg': "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.delivered_status:
            return Response({'msg': "Sorry, can't cancel the order as it has been delivered!"})

        amt = order.amount
        curr_time = timezone.now()
        # print(curr_time-order.created_at)
        time_diff = curr_time - order.created_at
        minutes_diff = int(time_diff.total_seconds() / 60)
        # print(minutes_diff)

        if minutes_diff > 60:
            return Response({'msg': "Sorry, can't cancel the order as it has been more than 60 minutes since ordering!"})

        order.delete()

        body = email_draft_delete(order_id, order.first_name+' '+order.last_name, amt)

        data = {
            'subject': 'Order Deletion - Your Order Has been Deleted 🛒',
            'body': body,
            'to_email': request.user.email
        }
        Util.send_email(data)
        return Response({'msg': "Your order has been successfully cancelled!"})
