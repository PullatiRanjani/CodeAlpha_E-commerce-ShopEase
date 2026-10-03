from django.contrib import admin
from django.urls import path

from store import views


# IMPORTANT:
# Admin session and customer session separate hosts lo maintain avvadanki
# Admin "View site" button customer site ki 127.0.0.1 URL open chestundi.
admin.site.site_url = "http://localhost:8000/admin/"


urlpatterns = [
    path(
    "admin/shop-preview/",
    views.admin_shop_preview,
    name="admin_shop_preview"
),
    # Custom admin live orders page
    path(
        "admin/live-orders/",
        views.live_orders,
        name="live_orders"
    ),

    # Django admin
    path(
        "admin/",
        admin.site.urls
    ),

    # Customer website
    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "product/<int:pk>/",
        views.product_detail,
        name="product_detail"
    ),

    # Cart
    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    path(
        "cart/add/<int:pk>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/update/<int:pk>/",
        views.update_cart,
        name="update_cart"
    ),

    path(
        "cart/remove/<int:pk>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    # Checkout
    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    # Orders
    path(
        "orders/",
        views.orders,
        name="orders"
    ),

    # Authentication
    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # Reviews
    path(
        "product/<int:pk>/review/",
        views.add_review,
        name="add_review"
    ),
]