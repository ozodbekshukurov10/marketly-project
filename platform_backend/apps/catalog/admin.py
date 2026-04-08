from django.contrib import admin

from .models import Category, Discount, Product, ProductImage


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Discount)
