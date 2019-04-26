"""
    This module defines the consumer class
    Consumers classes are similar to views for websockets

 """
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    """
        Here we define our consumer class
        We are going to do the async implementation for improved
        ..perfomance

     """

    async def connect(self):

        """
           Subscribe to notifications
         """
        self.username = self.scope['url_route']['kwargs']

        self.notification_group_name = '%s' % self.username['group']
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        Unsubscribe from notifications
        """

        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name
        )

    async def notify(self, event):
        """
            Sends notification to web socket
         """
        data_to_send = {'type': event['type'], 'message': event['message']}

        # Send message to WebSocket
        await self.send(text_data=json.dumps(data_to_send))

    @staticmethod
    async def send_socket_notification(content):
        """
        Calls the notify method to send notifications
        ..to a chosen channel_layer
        """
        channel_layer = get_channel_layer()

        await channel_layer.group_send(
            content['send_to'][0],
            {
                'type': 'notify',
                'message': content['message']
            }
        )
