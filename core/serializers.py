import random, string
from rest_framework import serializers
from .models import (
    User, Category, Product, Order, OrderItem, Cart, CartItem, Shipping, Payment, Coupon, Review, Wishlist, Notification, Blog, Configuration, Contact, FAQ, Tax, Subscription,Refund, Analytics
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# class VendorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vendor
#         fields = '__all__'

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
        fields = ['id', 'name', 'customer', 'shipping_address', 'products', 'total_price']

    def get_products(self, obj):
        order_items = obj.item.all()
        serialized_items = []
        for item in order_items:
            serialized_item = {
                'product': item.product.id,
                'quantity': item.quantity
            }
            serialized_items.append(serialized_item)
        return serialized_items

class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer', 'shipping_address', 'products', 'total_price']

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

# class OrderSerializer(serializers.ModelSerializer):
#     # customer = UserSerializer(read_only=True)
#     products = ProductSerializer(many=True)
    
#     class Meta:
#         model = Order
#         fields = '__all__'

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True ,read_only=True)

    class Meta:
        model = Wishlist
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class AnalyticsSerializer(serializers.ModelSerializer):
    popular_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Analytics
        fields = '__all__'

class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class RefundSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Refund
        fields = '__all__'

