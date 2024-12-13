from django.contrib import admin
from .models import (
    Category,
    MenuItem,
    Variant,
    Staff,
    Order,
    OrderItem,
    Subcategory,
    Client,
)

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(MenuItem)
admin.site.register(Variant)
admin.site.register(Staff)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Client)
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id",)
