from django.db.models import SET_NULL, Model, CharField, BigAutoField, ForeignKey, CASCADE, TextChoices



class UsersModels(Model):

    class UserRole(TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        ADMIN = "ADMIN", "Admin"
        DELIVERY_AGENT = "DELIVERY_AGENT", "Delivery Agent"
        MANAGER = "MANAGER", "Manager"

    id = BigAutoField(primary_key=True)

    firstName = CharField(max_length=50)
    lastName = CharField(max_length=50)

    username = CharField(max_length=50, unique=True, blank=False)
    role = CharField(
        max_length=30,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER
    )
    
    email = CharField(max_length=50, unique=True, blank=False)
    password = CharField(max_length=250)


    class Meta:
        db_table = "users"

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.username


class AddressModels(Model):
    id = BigAutoField(primary_key=True)
    users = ForeignKey(
        UsersModels,
        on_delete=CASCADE,
        related_name="addresses",
        db_column="users_id",
        null=True
    )

    longitude = CharField(max_length=50)
    latitude = CharField(max_length=50)

    pincode = CharField(max_length=6)
    state = CharField(max_length=100)
    city = CharField(max_length=100)
    addressLine = CharField(max_length=255)

    class Meta:
        db_table = "address"

    def __str__(self):
        return str(self.id)
