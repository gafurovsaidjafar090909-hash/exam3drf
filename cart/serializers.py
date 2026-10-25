
from rest_framework import serializers
from .models import *


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name',read_only=True)
    product_price = serializers.ReadOnlyField(source='product.price')
    item_total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id','product','product_name','product_price','quantity','item_total']

    def get_item_total(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']
    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())
    


class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name',read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','product','product_name','quantity','price']



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id','user','items','total_price','status','created_at',]
        read_only_fields = ['id','user','items','total_price','status','created_at',]




class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status']
        read_only_fields = ['id']

    def validate_status(self, value):
        if value not in Order.Status.values:
            raise serializers.ValidationError('Статус должен быть pending, processing или cancelled.')
        return value