from django.urls import path
from .views import UserProfileView, OrdersDelivery

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name="Delivery_Man_Profile"),
    path('ViewOrders/', OrdersDelivery.as_view(), name="Orders_to_be_delivered"),
]
