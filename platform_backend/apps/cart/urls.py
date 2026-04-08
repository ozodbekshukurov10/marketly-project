from django.urls import path

from .views import CartDetailView, CartItemManageView


urlpatterns = [
    path("", CartDetailView.as_view(), name="cart-detail"),
    path("items/", CartItemManageView.as_view(), name="cart-items"),
]
