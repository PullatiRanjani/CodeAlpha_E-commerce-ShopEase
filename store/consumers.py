from channels.generic.websocket import AsyncJsonWebsocketConsumer


class AdminLiveConsumer(
    AsyncJsonWebsocketConsumer
):

    group_name = "shopease_live_admins"

    async def connect(self):

        user = self.scope.get("user")

        if (
            not user
            or not user.is_authenticated
            or not user.is_staff
        ):
            await self.close(code=4403)
            return

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        await self.send_json({
            "event": "connection",
            "message": "Live connection active"
        })

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def live_event(self, event):

        await self.send_json(
            event["payload"]
        )


class ProductReviewConsumer(
    AsyncJsonWebsocketConsumer
):

    async def connect(self):

        self.product_id = (
            self.scope["url_route"]["kwargs"]
            ["product_id"]
        )

        self.group_name = (
            f"product_{self.product_id}_reviews"
        )

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        await self.send_json({
            "event": "connection",
            "message": "Review connection active"
        })

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def review_event(self, event):

        await self.send_json(
            event["payload"]
        )