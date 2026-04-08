from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity", "unit_price")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "status", "total_amount", "shipping_address", "items", "created_at")

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(user=self.context["request"].user, **validated_data)
        total = 0
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
            total += item["unit_price"] * item["quantity"]
        order.total_amount = total
        order.save(update_fields=["total_amount", "updated_at"])
        return order
