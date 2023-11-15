# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class SoundConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the 'sounds' group when the WebSocket connects
        await self.channel_layer.group_add("sounds", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the 'sounds' group when the WebSocket disconnects
        await self.channel_layer.group_discard("sounds", self.channel_name)

    # This handler is called when data is sent over the WebSocket
    async def receive(self, text_data):
        # Normally, we would handle incoming data here, such as chat messages.
        pass

    # This handler is called when the group 'sounds' sends a message
    async def sound_message(self, event):
        # Send a message down the WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
