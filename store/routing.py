from django.urls import path

from .consumers import (
    AdminLiveConsumer,
    ProductReviewConsumer
)


websocket_urlpatterns = [

    path(
        "ws/admin/live-orders/",
        AdminLiveConsumer.as_asgi()
    ),

    path(
        "ws/product/<int:product_id>/reviews/",
        ProductReviewConsumer.as_asgi()
    ),

]