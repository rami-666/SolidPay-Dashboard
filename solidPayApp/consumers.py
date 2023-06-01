from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings
from django.core.cache import cache
from solidPayApp.models import (
    paymentRequest,
    USDPaymentRequest
)
from asgiref.sync import async_to_sync, sync_to_async
import json

class PaymentStatusConsumer(AsyncWebsocketConsumer):
    def get_entry(self, addy, newChannel):
        temp = paymentRequest.objects.get(createdAddress=addy)
        temp.channel = newChannel
        temp.save()
        print("saved!")


    async def connect(self):
        self.address = self.scope['url_route']['kwargs']["address"]
        if self.address:

            await database_sync_to_async(self.get_entry)(addy = self.address, newChannel = self.channel_name)
            await self.channel_layer.group_add(self.address, self.channel_name)

            await self.accept()
        else:
            self.close()

        print("CONNECTED: ", self.scope['url_route']['kwargs'])


    async def receive(self, text_data):
        print("recieve called")
        pass

    async def disconnect(self, close_code):
        print("CLOSING CONNECTION WITH: ", self.address)
        if self.address:
            await self.channel_layer.group_discard(self.address, self.channel_name)

    async def notify_payment(self, event):
        print("SENDING NOTIFICATION TO: ", self.address)
        message = event['message']

        await self.send(text_data=message)

class USDPaymentStatusConsumer(AsyncWebsocketConsumer):
    def get_entry(self, addy, newChannel):
        temp = USDPaymentRequest.objects.get(createdAddress=addy)
        temp.channel = newChannel
        temp.save()
        print("saved!")


    async def connect(self):
        self.address = self.scope['url_route']['kwargs']["address"]
        if self.address:

            await database_sync_to_async(self.get_entry)(addy = self.address, newChannel = self.channel_name)
            await self.channel_layer.group_add(self.address, self.channel_name)

            await self.accept()
        else:
            self.close()

        print("CONNECTED: ", self.scope['url_route']['kwargs'])


    async def receive(self, text_data):
        print("recieve called")
        pass

    async def disconnect(self, close_code):
        print("CLOSING CONNECTION WITH: ", self.address)
        if self.address:
            await self.channel_layer.group_discard(self.address, self.channel_name)

    async def notify_payment(self, event):
        print("SENDING NOTIFICATION TO: ", self.address)
        message = event['message']

        await self.send(text_data=message)