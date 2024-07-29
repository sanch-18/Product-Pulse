from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name="Delivery_Man_Profile"),
]
