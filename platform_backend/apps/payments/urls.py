from django.urls import path

from .views import PaymentCreateView, PaymentProvidersView


urlpatterns = [
    path("", PaymentCreateView.as_view(), name="payment-create"),
    path("providers/", PaymentProvidersView.as_view(), name="payment-providers"),
]
