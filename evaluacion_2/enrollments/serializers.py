from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from courses.serializers import CourseSerializer

class CartItemSerializer(serializers.ModelSerializer):
    course_detail = CourseSerializer(source='course', read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'course', 'course_detail', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    course_detail = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'course', 'course_detail', 'price_at_purchase']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'items']
