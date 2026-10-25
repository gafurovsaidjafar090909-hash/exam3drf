from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
from .views import ProductSearchView

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='product')

urlpatterns = [
    path('products-list/', ProductListView.as_view(), name='product-list'),
    path('products-detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products-search/', ProductSearchView.as_view(), name='product-search'),
]

urlpatterns += router.urls