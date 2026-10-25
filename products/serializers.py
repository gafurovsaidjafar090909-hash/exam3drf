from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','description','created_at']
        read_only_fields=['id','created_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','category','name','description','price','stock','created_at']
        read_only_fields=['id','created_at']