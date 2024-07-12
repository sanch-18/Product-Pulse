from django.urls import path, include

from . import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('categories/', views.Category_view.as_view()),
    path('product/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('product/<slug:category_slug>/', views.CategoryDetail.as_view()),
    path('search/', views.Search.as_view()),
]