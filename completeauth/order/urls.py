from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.OrdersList.as_view()),
    path('cart/', views.OrderCart.as_view()),
    path('DeleteOrder/', views.DeleteCart.as_view()),
]