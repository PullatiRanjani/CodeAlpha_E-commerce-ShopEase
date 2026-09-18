from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone


def order_payload(order):

    return {
        "event": "order_updated",
        "order_number": order.order_number,
        "customer": order.full_name,
        "total": float(order.total),
        "status": order.status,
        "created_at": timezone.localtime(
            order.created_at
        ).strftime("%d %b %Y, %I:%M %p"),

        "items": [
            {
                "name": item.product.name,
                "quantity": item.quantity
            }
            for item in order.items.select_related("product").all()
        ],
    }


def broadcast_order(order, event="order_updated"):

    channel_layer = get_channel_layer()

    payload = order_payload(order)

    payload["event"] = event

    async_to_sync(
        channel_layer.group_send
    )(
        "shopease_live_admins",
        {
            "type": "live_event",
            "payload": payload,
        }
    )


def broadcast_review(review):

    product = review.product

    payload = {
        "event": "review",

        "review_id": review.id,

        "product_id": product.id,

        "product": product.name,

        "rating": review.rating,

        "average_rating": product.rating,

        "review_count": product.review_count,

        "reviewer": review.user.username,

        "comment": review.comment,

        "created_at": timezone.localtime(
            review.updated_at
        ).strftime("%d %b %Y"),
    }

    channel_layer = get_channel_layer()

    async_to_sync(
        channel_layer.group_send
    )(
        f"product_{product.id}_reviews",
        {
            "type": "review_event",
            "payload": payload,
        }
    )