from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.orders.models import Order

from .serializers import PaymentTransactionSerializer


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(status="successful")
        order = Order.objects.get(pk=payment.order_id)
        order.status = "paid"
        order.save(update_fields=["status", "updated_at"])


class PaymentProvidersView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "fake": {"enabled": True, "mode": "test"},
                "click": {"enabled": False, "integration_structure_ready": True},
                "payme": {"enabled": False, "integration_structure_ready": True},
            }
        )
