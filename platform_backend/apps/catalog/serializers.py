from rest_framework import serializers

from .models import Category, Discount, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "is_primary")


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ("id", "percentage", "starts_at", "ends_at")


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    discount = DiscountSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "seller",
            "category",
            "title",
            "slug",
            "description",
            "price",
            "stock",
            "is_active",
            "images",
            "discount",
            "created_at",
        )
        read_only_fields = ("seller",)

    def create(self, validated_data):
        validated_data["seller"] = self.context["request"].user
        return super().create(validated_data)
