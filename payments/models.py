from django.db import models
from django.conf import settings


class Client(models.Model):
    name = models.CharField(max_length=80)
    surname = models.CharField(max_length=80, null=True)
    email = models.EmailField()
    birthday = models.DateField(null=True, blank=True)


class Payment(models.Model):
    order_id = models.CharField(max_length=80, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(
        max_length=20, default="pending"
    )  # e.g., pending, success, failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.order_id} - {self.status}"


class Staff(models.Model):
    chat_id = models.CharField(max_length=255, unique=True)


class Category(models.Model):
    order = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    name_pt = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    order = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category,
        related_name="subcategories",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    name_pt = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.category.name})"


class MenuItem(models.Model):
    category = models.ForeignKey(
        Category, related_name="items", on_delete=models.CASCADE, blank=True, null=True
    )
    subcategory = models.ForeignKey(
        Subcategory,
        related_name="items",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255)
    name_pt = models.CharField(max_length=255, blank=True, null=True)
    description_pt = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="media/images", blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True)
    ingredients_pt = models.TextField(blank=True, null=True)
    volume = models.CharField(max_length=80, blank=True, null=True)
    allergens = models.TextField(blank=True, null=True)
    allergens_pt = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_category(self):
        if self.subcategory:
            return f"{self.subcategory.name}"
        return f"{self.category.name}" if self.category else "no category"


class Variant(models.Model):
    menu_item = models.ForeignKey(
        MenuItem, related_name="variants", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    name_pt = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    description_pt = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.menu_item.name}"


class Order(models.Model):
    order_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    table_id = models.IntegerField(null=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="orders", blank=True, null=True
    )

    def __str__(self):
        return f"Order {self.created_at}"

    @property
    def formatted_created_at(self):
        # Форматируем дату как строку
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(
        Variant, on_delete=models.SET_NULL, null=True, blank=True
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        variant_name = f" ({self.variant.name})" if self.variant else ""
        return f"{self.quantity} x {self.menu_item.name}{variant_name} in Order {self.order.id}"
