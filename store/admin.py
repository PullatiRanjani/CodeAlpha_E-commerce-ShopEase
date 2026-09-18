from django.contrib import admin

from .models import (
    Category,
    Product,
    CartItem,
    Order,
    OrderItem,
    Review,
)


# =========================================================
# CATEGORY
# =========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    search_fields = (
        "name",
    )


# =========================================================
# PRODUCT
# =========================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "stock",
        "featured",
        "rating_display",
        "review_count_display",
        "created_at",
    )

    list_filter = (
        "category",
        "featured",
    )

    search_fields = (
        "name",
        "description",
    )

    readonly_fields = (
        "rating_display",
        "review_count_display",
        "created_at",
    )

    def rating_display(self, obj):
        return obj.rating

    rating_display.short_description = "Customer Rating"

    def review_count_display(self, obj):
        return obj.review_count

    review_count_display.short_description = "Reviews"


# =========================================================
# CART ITEM
# =========================================================

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "product",
        "quantity",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "product__name",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )


# =========================================================
# ORDER ITEM INLINE
# =========================================================

class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    readonly_fields = (
        "product",
        "quantity",
        "price",
        "line_total",
    )

    def line_total(self, obj):
        return obj.line_total

    line_total.short_description = "Total"


# =========================================================
# ORDER
# =========================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "user",
        "full_name",
        "total",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "full_name",
        "email",
        "user__username",
    )

    readonly_fields = (
        "order_number",
        "user",
        "full_name",
        "email",
        "address",
        "city",
        "postal_code",
        "total",
        "created_at",
    )

    inlines = [
        OrderItemInline
    ]


# =========================================================
# REVIEWS
# =========================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "user",
        "rating",
        "comment",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "rating",
        "created_at",
    )

    search_fields = (
        "product__name",
        "user__username",
        "comment",
    )

    readonly_fields = (
        "product",
        "user",
        "rating",
        "comment",
        "created_at",
        "updated_at",
    )