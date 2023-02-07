# from rest_framework import serializers
# from .models import Product, Cart, Category, Order
#
#
# class ProductSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Product
#         fields = "__all__"
#
#
# class CartSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Cart
#         fields = "__all__"
#
#
# class CategorySerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Category
#         fields = "__all__"
#
#
# class OrderSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         models = Order
#         fields = '__all__'
#
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product, Cart, Order, Category


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'vendor', 'name', 'price', 'description']


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        models = Order
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
