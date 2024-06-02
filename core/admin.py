from django.contrib import admin

# Register your models here.
from .models import (
    User, Category, Product, Order, OrderItem, Cart, CartItem, Payment
)

admin.site.register((User, Category, Product, Order, OrderItem, Cart, CartItem, Payment))