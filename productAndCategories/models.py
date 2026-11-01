from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import DateTimeField, DecimalField, Model, CharField, PositiveIntegerField, SlugField, TextField, URLField, BooleanField, Index, BigAutoField, ForeignKey, PROTECT

# Create your models here.


class CategoriesModel(Model):

    name = CharField(max_length=100, unique=True)
    slug = SlugField(max_length=100, unique=True)
    descriptions = TextField(blank=True)

    image_urls = URLField(blank=True)
    is_active = BooleanField(default=True)

    class Meta:
        db_table = "categories"
        indexes = [
            Index(
                fields=["name", "slug"]
            )
        ]

    def __str__(self):
        return self.name


class ProductModel(Model):

    id = BigAutoField(primary_key=True)
    category = ForeignKey(
        CategoriesModel,
        on_delete=PROTECT,
        related_name="product"
    )

    name = CharField(max_length=100)
    slug = SlugField(max_length=100, unique=True)
    unit = CharField(max_length=50)
    stock_quantity = PositiveIntegerField(default=0, validators=[
        MinValueValidator(1), MaxValueValidator(1000)
    ])

    description = TextField(blank=True)
    price = DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    image_url = URLField(blank=True)
    is_active = BooleanField(default=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.name
