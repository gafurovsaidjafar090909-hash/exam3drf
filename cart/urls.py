from django.urls import path
from .views import *
from drf_yasg.views import get_schema_view

urlpatterns = [
    path('', MyCartView.as_view(), name='my-cart'),
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('items/<int:pk>/update/',UpdateCartItemView.as_view(),name='update-cart-item'),
    path('items/<int:pk>/delete/',DeleteCartItemView.as_view(),name='delete-cart-item'),
     path('checkout/', CreateOrderView.as_view(), name='checkout'),
     path('my-orders/', MyOrdersView.as_view(), name='my-orders'),
     path('my-orders/<int:pk>/',OrderDetailView.as_view(),name='order-detail'),
     path('my-orders/<int:pk>/cancel/',CancelOrderView.as_view(),name='cancel-order'),
     path('admin/orders/<int:pk>/status/',AdminOrderStatusUpdateView.as_view(),name='admin-order-status'),
]