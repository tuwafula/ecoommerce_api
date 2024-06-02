from django.urls import path, include
from rest_framework import routers
from .views import (
    UserViewSet, CategoryViewSet, ProductViewSet, OrderItemViewSet, OrderViewSet, DashboardView, OrderViewSet2, OrderViewSet3
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'update-orders', OrderViewSet3)
router.register(r'get-orders', OrderViewSet2)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('dashboard/', DashboardView.as_view())
]
