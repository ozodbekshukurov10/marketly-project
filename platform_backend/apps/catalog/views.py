from rest_framework import permissions, viewsets

from apps.common.permissions import IsSeller

from .models import Category, Discount, Product
from .serializers import CategorySerializer, DiscountSerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ("name",)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category", "seller").prefetch_related("images").all()
    serializer_class = ProductSerializer
    filterset_fields = ("category", "is_active", "seller")
    search_fields = ("title", "description")
    ordering_fields = ("created_at", "price", "title")

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsSeller()]
        return [permissions.AllowAny()]


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.select_related("product").all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated]
