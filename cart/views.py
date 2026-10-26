
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser


class MyCartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    


class AddToCartView(generics.CreateAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        cart = Cart.objects.get_or_create(user=request.user)[0]
        item = CartItem.objects.filter(cart=cart,product=product).first()
        if item:
            item.quantity += quantity
            item.save()
        else:
            CartItem.objects.create(cart=cart,product=product,quantity=quantity)
        return Response({'message': 'Product added to cart'},status=201)


class UpdateCartItemView(generics.UpdateAPIView):
    serializer_class = UpdateCartItemSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)



class DeleteCartItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)




class CreateOrderView(generics.GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')
        if not cart_items.exists():
            return Response({'error': 'Your cart is empty'},status=status.HTTP_400_BAD_REQUEST)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user,total_price=total_price)
        for item in cart_items:
            OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity,price=item.product.price)
        cart_items.delete()
        serializer = self.get_serializer(order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)



class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('created_at')



class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)




class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        order = get_object_or_404(Order,pk=pk,user=request.user)
        if order.status != Order.Status.PENDING:
            return Response({'error': 'zakaz dar sanjishay yo atminit shdagiay'},status=status.HTTP_400_BAD_REQUEST)
        order.status = Order.Status.CANCELLED
        order.save(update_fields=['status'])
        return Response(
            {'message': 'zakaz otminit shud','order_id': order.id,'status': order.status},status=status.HTTP_200_OK)



class AdminOrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = [IsAdminUser]