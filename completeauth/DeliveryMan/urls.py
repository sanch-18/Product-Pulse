from django.urls import path
from .views import UserProfileView, OrdersDelivery, AllOrdersDelivery

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name="Delivery_Man_Profile"),
    path('ViewAllOrders/', AllOrdersDelivery.as_view(), name="Orders_to_be_delivered"),
    path('ViewOrdersToBeDelivered/', OrdersDelivery.as_view(), name="Orders_to_be_delivered"),
]
