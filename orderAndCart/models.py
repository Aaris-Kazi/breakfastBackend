from django.db.models import CASCADE, PROTECT, Q, CheckConstraint, DateTimeField, ForeignKey, Index, Model, BigAutoField, CharField, DecimalField, PositiveIntegerField, TextChoices, UniqueConstraint
from productAndCategories.models import ProductModel
from userAuth.models import AddressModels, UsersModels
# Create your models here.


class CartModel(Model):
    class CartStatus(TextChoices):
        ACTIVE = "ACTIVE", "Active"
        CONVERTED = "CONVERTED", "Converted"
        ABANDONED = "ABANDONED", "Abandoned"

    id = BigAutoField(primary_key=True)
    users = ForeignKey(
        UsersModels,
        on_delete=PROTECT,
        related_name="carts",
        db_column="users_id",
    )

    status = CharField(
        max_length=20,
        choices=CartStatus.choices,
        default=CartStatus.ACTIVE,
    )

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "cart"
        indexes = [
            Index(fields=["users", "status"]),
        ]

    def __str__(self):
        return f"Cart {self.id} - {self.status}"


class CartItemModel(Model):
    id = BigAutoField(primary_key=True)

    cart = ForeignKey(
        CartModel,
        on_delete=CASCADE,
        related_name="items",
        db_column="cart_id",
    )

    product = ForeignKey(
        ProductModel,
        on_delete=PROTECT,
        related_name="cart_items",
        db_column="product_id",
    )

    quantity = PositiveIntegerField(default=1)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "cart_item"
        constraints = [
            UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_per_cart",
            ),
            CheckConstraint(
                condition=Q(quantity__gte=1),
                name="cart_item_quantity_at_least_one",
            ),
        ]

    def __str__(self):
        return f"Cart {self.cart_id} - Product {self.product_id} x {self.quantity}"


class OrderModel(Model):
    class OrderStatus(TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        PROCESSING = "PROCESSING", "Processing"
        OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY", "Out for delivery"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

    class PaymentStatus(TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    id = BigAutoField(primary_key=True)

    users = ForeignKey(
        UsersModels,
        on_delete=PROTECT,
        related_name="orders",
        db_column="users_id",
    )

    address = ForeignKey(
        AddressModels,
        on_delete=PROTECT,
        related_name="orders",
        db_column="address_id",
    )

    status = CharField(
        max_length=30,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    payment_status = CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )

    subtotal = DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    delivery_fee = DecimalField(
        max_digits=10, decimal_places=2, default=20
    )
    total_amount = DecimalField(
        max_digits=12, decimal_places=2, default=0
    )

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]
        indexes = [
            Index(fields=["users", "created_at"]),
            Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Order {self.id} - {self.status}"


class OrderItemModel(Model):
    id = BigAutoField(primary_key=True)

    order = ForeignKey(
        OrderModel,
        on_delete=CASCADE,
        related_name="items",
        db_column="order_id",
    )

    product = ForeignKey(
        ProductModel,
        on_delete=PROTECT,
        related_name="order_items",
        db_column="product_id",
    )

    # Snapshot values preserve the purchase history.
    product_name = CharField(max_length=255)
    unit_price = DecimalField(max_digits=10, decimal_places=2)
    quantity = PositiveIntegerField()

    class Meta:
        db_table = "order_item"
        constraints = [
            CheckConstraint(
                condition=Q(quantity__gte=1),
                name="order_item_quantity_at_least_one",
            ),
            CheckConstraint(
                condition=Q(unit_price__gte=0),
                name="order_item_price_nonnegative",
            ),
        ]

    @property
    def line_total(self):
        return self.unit_price * self.quantity
