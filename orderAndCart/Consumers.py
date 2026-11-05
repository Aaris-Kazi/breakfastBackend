import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

log = logging.getLogger(__name__)

class CartConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            self.user = self.scope["user"]
            if not self.user.is_authenticated:
                await self.close()
                return

            self.group_name = f"cart_{self.user.id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            log.info(f"WebSocket connection received for user: {self.user}")
            log.info(f"WebSocket connection received for user: {self.user.id}")
            await self.accept()
            await asyncio.sleep(5)  # Optional: Wait for a moment before sending the message
            await self.send(text_data="Connected successfully!")
        except Exception as e:
            log.error(f"Error during WebSocket connection: {e}")
            await self.close()
            return

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        log.info(f"Disconnected: {close_code}")

    async def cart_updated(self, event):
            log.info(f"Cart updated event received: {event}")
            await self.send(text_data=json.dumps({
                "type": "CART_UPDATED",
                "data": event["data"]
            }))
