from rest_framework import viewsets
from .models import (
    User, Category, Product, Order, OrderItem, Cart, CartItem, Shipping, Payment, Coupon, Review, Wishlist, Notification, Blog, Configuration, Contact, FAQ, Tax, Subscription,Refund, Analytics
    )
from .serializers import (
    UserSerializer, CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, CartItemSerializer, CartSerializer, ShippingSerializer, PaymentSerializer, CouponSerializer, WishlistSerializer, NotificationSerializer, BlogSerializer, ConfigurationSerializer, ContactSerializer, FAQSerializer, TaxSerializer, SubscriptionSerializer, RefundSerializer, ReviewSerializer, AnalyticsSerializer, OrderSerializer2, OrderSerializer3
)

from rest_framework.views import APIView
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderViewSet2(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer2

class OrderViewSet3(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer3

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class DashboardView(APIView):

    def get(self, request):
        users_count = User.objects.count()
        orders_count = Order.objects.count()
        products_count = Product.objects.count()
        categories_count = Category.objects.count()

        return Response({'data': {'users': users_count, 'orders':orders_count, 'products':products_count, 'categories':categories_count}})

