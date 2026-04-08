from django.db import transaction
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartItemCreateSerializer, CartSerializer


class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart


class CartItemManageView(generics.GenericAPIView):
    serializer_class = CartItemCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=serializer.validated_data["product"],
            defaults={"quantity": serializer.validated_data["quantity"]},
        )
        if not created:
            item.quantity += serializer.validated_data["quantity"]
            item.save(update_fields=["quantity", "updated_at"])
        return Response({"status": "ok", "item_id": str(item.id)})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get("product")
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response({"status": "deleted"})
