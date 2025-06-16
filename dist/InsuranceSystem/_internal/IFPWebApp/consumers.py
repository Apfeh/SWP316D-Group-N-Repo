# IFPWebApp/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('admin_notifications', self.channel_name)
        print("WebSocket connected")  # Debug
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('admin_notifications', self.channel_name)
        print("WebSocket disconnected")  # Debug

    async def send_notification(self, event):
        print(f"Sending notification: {event['message']} (ID: {event['id']})")  # Debug
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'created_at': event['created_at'],
            'id': event['id']
        }))