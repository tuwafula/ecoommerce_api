from django.contrib import admin

# Register your models here.
from .models import (
    User, Vendor, Category, Product, Order, OrderItem, Cart, CartItem, Shipping, Payment, Coupon, Review, Wishlist, Notification, Blog, Configuration, Contact, FAQ, Tax, Subscription,Refund, Analytics
)

admin.site.register((User, Vendor, Category, Product, Order, OrderItem, Cart, CartItem, Shipping, Payment, Coupon, Review, Wishlist, Notification, Blog, Configuration, Contact, FAQ, Tax, Subscription,Refund, Analytics))