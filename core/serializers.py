import random, string
from rest_framework import serializers
from .models import (
    User, Category, Product, Order, OrderItem, Cart, CartItem, Payment, 
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer2(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'name', 'customer', 'shipping_address', 'city', 'products', 'total_price', 'status', 'created_at', 'updated_at']

    def get_products(self, obj):
        order_items = obj.item.all()
        serialized_items = []
        for item in order_items:
            serialized_item = {
                'product': ProductSerializer(item.product).data,
                'quantity': item.quantity
            }

            
            serialized_items.append(serialized_item)
        return serialized_items

class OrderSerializer3(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['customer', 'shipping_address', 'city', 'products', 'total_price', 'status']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer', 'shipping_address', 'city', 'products', 'total_price', 'status']

    def create(self, validated_data):
        products_data = validated_data.pop('products')

        order_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        validated_data['name'] = f"Order-# {order_name}"

        order = Order.objects.create(**validated_data)

        total_price = 0  

        for product_data in products_data:
           
            product = product_data['product']  
            product_quantity = product_data['quantity']
            total_price += product.price * product_quantity
            OrderItem.objects.create(order=order, product=product, quantity=product_quantity)

        order.total_price = total_price
        order.save()

        return order


