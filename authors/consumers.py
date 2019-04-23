from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.layers import get_channel_layer


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    """

    async def connect(self):
        """This method will allow a new user to connect to a notification
            group
        """

        self.notification_kwargs = self.scope['url_route']['kwargs']
        stream = self.notification_kwargs.get('stream', 'default')
        self.notification_group_name = stream
        self.groups.append(self.notification_group_name)
        # join the notification group eg _new articles
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Disconnects a user from a notification group

        Arguments:
            close_code {[type]} -- [Reason for closure could be
            connection(managed by asgi)]
        """

        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name
        )

    async def notify(self, content, **kwargs):
        """Send triggered notifications
        content = {"message":"Message is a must" ,
        'type':"",
        "send Email": "allows us to hook email sender here ",
        }
        """
        sendData = {'type': content['type'], 'message': content['message']}
        await self.send(text_data=json.dumps(sendData))

    async def receive(self, text_data, **kwargs):
        """Reeives messages from the wire/online from the user
        """

        self.notification_kwargs = self.scope['url_route']['kwargs']
        stream = self.notification_kwargs.get('stream', 'default')
        self.notification_group_name = stream
        await self.channel_layer.group_send(
            self.notification_group_name,
            {
                'type': 'notify',
                'message': text_data
            }
        )


async def send_notification(content):
    """uses the notify method in NotificationConsumer
        class to send notifications
        import the method anywhere one needs to send notications
    Arguments
        content {[dict]} -- [must include
        {'send_to':'list of groups to send notification to',
        'message': 'The message to send to the group'}
        ]
    """

    channel_layer = get_channel_layer()
    for group_name in content['send_to']:
        await channel_layer.group_send(
            group_name,
            {
                'type': 'notify',
                'message': content['message']
            }
        )
