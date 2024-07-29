from rest_framework.permissions import BasePermission

class IsDeliveryman(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (not request.user.isDeliveryMan)

class IsNotDeliveryMan(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.isDeliveryMan