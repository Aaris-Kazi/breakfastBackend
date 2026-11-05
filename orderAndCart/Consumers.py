import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CartConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            print("WebSocket connection received")
            await self.accept()
            await self.send(text_data="Connected successfully!")
        except Exception as e:
            print(f"Error during WebSocket connection: {e}")
            await self.close()
            return

    async def disconnect(self, close_code):
        print("Disconnected:", close_code)

# class CartConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         self.user = self.scope["user"]

#         if not self.user.is_authenticated:
#             await self.close()
#             return

#         self.group_name = f"cart_{self.user.id}"

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         if hasattr(self, "group_name"):
#             await self.channel_layer.group_discard(
#                 self.group_name,
#                 self.channel_name
#             )

#     async def cart_updated(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "CART_UPDATED",
#             "data": event["data"]
#         }))