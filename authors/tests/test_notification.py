import pytest
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json
from channels.testing import WebsocketCommunicator
from authors.routing import application


class NotificationConsumerTest(APITestCase):

    @pytest.mark.asyncio
    async def test_send_and_receive(self):
        communicator = WebsocketCommunicator(
            application, "/api/notifications/test/")
        connected, subprotocol = await communicator.connect()

        self.assertTrue(connected)

        await communicator.send_to(text_data="hello")
        response = await communicator.receive_from()
        self.assertEqual(response, "hello")
        await communicator.disconnect()
