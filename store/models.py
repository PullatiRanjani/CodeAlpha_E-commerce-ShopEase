import uuid
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def generate_order_number():
    return uuid.uuid4().hex


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):

    GENDER_CHOICES = [
        ("Boys", "Boys"),
        ("Girls", "Girls"),
        ("Men", "Men"),
        ("Women", "Women"),
        ("Unisex", "Unisex"),
    ]

    TYPE_CHOICES = [
        ("Jeans", "Jeans"),
        ("Shirt", "Shirt"),
        ("T-Shirt", "T-Shirt"),
        ("Top","Top"),
        ("Dress", "Dress"),
        ("Jacket", "Jacket"),
        ("Pants", "Pants"),
        ("Hoodie", "Hoodie"),
        ("Sweatshirt", "Sweatshirt"),
        ("Shoes", "Shoes"),
        ("Accessories", "Accessories"),
        ("Other", "Other"),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default="Unisex"
    )

    product_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        default="Other"
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    image_url = models.URLField(
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    featured = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def rating(self):
        reviews = self.reviews.all()

        if not reviews.exists():
            return 0

        total = sum(
            review.rating
            for review in reviews
        )

        return round(
            total / reviews.count(),
            1
        )

    @property
    def review_count(self):
        return self.reviews.count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


class CartItem(models.Model):
    """
    Each customer's cart is stored in the database.
    Therefore the cart belongs to the logged-in user,
    not to the browser session.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-updated_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product_cart"
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.product.name} × "
            f"{self.quantity}"
        )

    @property
    def line_total(self):
        return self.product.price * self.quantity


class Order(models.Model):

    STATUS_CHOICES = [
        ("Placed", "Placed"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    order_number = models.CharField(
        max_length=32,
        unique=True,
        editable=False,
        null=True,
        blank=True
    )

    full_name = models.CharField(
        max_length=200
    )

    email = models.EmailField()

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    postal_code = models.CharField(
        max_length=20
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Placed"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.order_number:
            self.order_number = generate_order_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"#{self.order_number}"

    class Meta:
        ordering = ["-created_at"]


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items"
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def line_total(self):
        return self.price * self.quantity

    def __str__(self):
        return (
            f"{self.product.name} × "
            f"{self.quantity}"
        )


class Review(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="product_reviews"
    )

    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["product", "user"],
                name="unique_user_product_review"
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.product.name} - "
            f"{self.rating}/5"
        )