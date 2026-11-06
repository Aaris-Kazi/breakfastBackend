from rest_framework.serializers import ValidationError

from .models import CartModel, CartItemModel, OrderModel, OrderItemModel
from productAndCategories.models import ProductModel
from userAuth.models import UsersModels
from userAuth.models import AddressModels
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from constants.AppConstants import AppConstants
import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class OrderCartService:

    logger = logging.getLogger(__name__)

    @transaction.atomic
    def createCart(self, data: dict, username):
        cart = CartModel.objects.get_or_create(users = UsersModels.objects.get(id = username.id) , status=CartModel.CartStatus.ACTIVE)[0]
        cartItem = CartItemModel.objects.create(
            cart=cart,
            product=ProductModel.objects.get(id=data.get('product_id')),
            quantity=data.get('quantity'),
        )

        return cart, cartItem

    def get_cart_size(self, cart_id):

        return CartItemModel.objects.filter(
            cart_id=cart_id
        ).count()

    def getCart(self, username: str):
        return CartItemModel.objects.filter(
            cart__users__username=username,
            cart__status=CartModel.CartStatus.ACTIVE
        ).select_related(
            "cart", "product", "cart__users"
        )

    @transaction.atomic
    def updateCart(self, username: str, pk: int, data: dict):
        try:
            quantity: int = data.get("quantity")
            if quantity is None or quantity < 0:
                raise ValidationError("Quantity negative or 0")

            if pk is None or pk < 0:
                raise ValidationError("pk negative or 0")

            cart = CartItemModel.objects.select_for_update().get(
                cart__users__username=username,
                cart__status=CartModel.CartStatus.ACTIVE,
                product__id=pk
            )
            if quantity > cart.product.stock_quantity:
                raise ValidationError(
                    f"Only few is left {cart.product.stock_quantity}")
            cart.quantity = quantity

            cart.save()
            return cart
        except ValidationError as e:
            self.logger.error(
                f"Validation occured in update due to {e.args[0]}")
            raise e
        except Exception as e:
            self.logger.error(
                f"Exception occured in update due to {e.args[0]}")
            raise e

    @transaction.atomic
    def deleteCart(self, username: str, pk: int):
        try:
            if pk is None or pk < 0:
                raise ValidationError("pk negative or 0")

            cart = CartItemModel.objects.select_for_update().get(
                cart__users__username=username,
                cart__status=CartModel.CartStatus.ACTIVE,
                product__id=pk
            )
            cart.delete()
            return cart
        except Exception as e:
            self.logger.error(f" Exception occured in {e.args[0]}")
            raise e

    @transaction.atomic
    def createOrder(self, username: str, data: dict):
        try:

            id = data.get("cart_id")
            addr_id = data.get("addr_id")
            cart = CartModel.objects.select_for_update().get(
                users__username=username,
                status=CartModel.CartStatus.ACTIVE,
                id=id
            )

            addr = AddressModels.objects.get(
                users=cart.users,
                id=addr_id
            )

            cartItem = CartItemModel.objects.select_for_update().filter(
                cart=cart
            ).order_by("product")

            if not cartItem:
                raise ValidationError("Cannot place empty cart")

            product_ids = sorted(
                items.product.id for items in cartItem
            )

            products = {
                product.id: product
                for product in ProductModel.objects
                .select_for_update()
                .filter(id__in=product_ids)
                .order_by("id")
            }

            subtotal = Decimal(AppConstants.DEFAULT_DELIVERY_FEE.value)

            for item in cartItem:
                product = products.get(item.product_id)

                if product is None:
                    raise ValidationError(
                        f"Product {item.product_id} no longer exists."
                    )

                if product.stock_quantity < item.quantity:
                    raise ValidationError(
                        f"Insufficient stock for {product.name}. "
                        f"Available: {product.stock_quantity}."
                    )

                subtotal += product.price * item.quantity

            # Replace this with your delivery-fee calculation.
            delivery_fee = Decimal("20.00")
            total_amount = subtotal + delivery_fee

            # 6. Create the order.
            order = OrderModel.objects.create(
                users=cart.users,
                address=addr,
                subtotal=subtotal,
                delivery_fee=delivery_fee,
                total_amount=total_amount,
                status=OrderModel.OrderStatus.PENDING,
                payment_status=OrderModel.PaymentStatus.PENDING,
            )

            # 7. Create order items and deduct stock.
            order_items = []

            for item in cartItem:
                product = products[item.product_id]

                order_items.append(
                    OrderItemModel(
                        order=order,
                        product=product,
                        product_name=product.name,
                        unit_price=product.price,
                        quantity=item.quantity,
                    )
                )

                product.stock_quantity -= item.quantity

            OrderItemModel.objects.bulk_create(order_items)
            ProductModel.objects.bulk_update(
                products.values(),
                ["stock_quantity"],
            )

            # 8. Mark the cart as converted.
            cart.status = CartModel.CartStatus.CONVERTED
            cart.save(update_fields=["status", "updated_at"])

            return order, cart

        except CartModel.DoesNotExist:
            self.logger.error(
                f"Validation CartModel does not exist for {username}")
            raise ValidationError(
                f"Validation CartModel does not exist for {username}")

        except AddressModels.DoesNotExist:
            self.logger.error(
                f"Validation AddressModels does not exist for {username}")
            raise ValidationError(
                f"Validation AddressModels does not exist for {username}")

        except Exception as e:
            self.logger.error(
                f"Validation occured in createOrder due to {e.args[0]}")
            raise e

    def getOrder(self, username: str, order_page:int = 1) -> OrderItemModel:
        three_months = timezone.now() - timedelta(days= (order_page * 90))
        order = OrderModel.objects.filter(
            users__username = username,
            created_at__gte = three_months
        ).order_by("-created_at")[0]

        orderItem = OrderItemModel.objects.filter(
            order = order
        )

        return orderItem

    @transaction.atomic
    def updateOrderStatus(self, username:str, orderId: str, paymentStatus: str = None, deliveryStatus: str = None):
        try:

            if deliveryStatus is None and paymentStatus is None:
                raise ValidationError("Both the parameter cannot be empty")

            order = OrderModel.objects.select_for_update().get(
                id=orderId
            )

            if paymentStatus is not None:
                order.payment_status = paymentStatus
            if deliveryStatus is not None:
                order.status = deliveryStatus

            order.save()


        except OrderModel.DoesNotExist:
            self.logger.error(
                f"Validation OrderModel does not exist for {orderId }")
            raise ValidationError(f"Validation OrderModel does not exist for {username}")

        except Exception as e:
            self.logger.error(
                f"Validation OrderModel does not exist for {e.args[0]}")
            raise ValidationError(f"Validation OrderModel due to :: {e.args[0]}")

    def notify_cart_updated(self, user_id, cart_data):
        self.logger.info(f"Notifying cart update for user {user_id} with data: {cart_data}")
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"cart_{user_id}",
            {
                "type": "cart.updated",
                "data": cart_data
            }
        )

    def notify_cart_size(self, user_id, size: int):
        self.logger.info(f"Notifying cart size update for user {user_id} with size: {size}")
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"cart_{user_id}",
            {
                "type": "cart.size.updated",
                "data": size
            }
        )
