from rest_framework.serializers import Serializer, IntegerField, CharField, DecimalField, SerializerMethodField, DateTimeField, ChoiceField
from productAndCategories.prodAndCatSerializer import ProductSerializer
from .models import OrderModel

class CartSerializer(Serializer):
    cart_id = IntegerField(required=False)
    product_id = IntegerField(required=True)
    quantity = IntegerField(required=True)


class CartItemSerializer(Serializer):
    id = IntegerField()
    status = CharField(max_length=255)


class CartUpdateSerializer(Serializer):
    quantity = IntegerField(required=True, min_value=1)


class CartResponseSerializer(Serializer):
    # cart = CartItemSerializer()
    product = ProductSerializer()
    quantity = IntegerField(required=False)


class OrderSerializer(Serializer):
    cart_id = IntegerField()
    addr_id = IntegerField()


class OrderResponseSerializer(Serializer):
    id = IntegerField(required=False)
    status = CharField(max_length=255)
    payment_status = CharField(max_length=255)
    delivery_fee = DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = DateTimeField()


class OrderItemResponseSerializer(Serializer):
    id = IntegerField(required=False)
    product = ProductSerializer()
    quantity = IntegerField(required=True)
    unit_price = DecimalField(max_digits=12, decimal_places=2, default=0)
    # delivery_fee = DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = DecimalField(
        source="line_total",
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )

    # def get_total_amount(self, obj):
    #      return obj.unit_price * obj.quantity

class OrderUpdateSerializer(Serializer):
    status = ChoiceField(
        choices=OrderModel.OrderStatus.choices,
        required = False
    )
    paymentStatus = ChoiceField(
        choices=OrderModel.PaymentStatus.choices,
        required = False
    )
