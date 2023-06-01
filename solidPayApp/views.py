import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import views
from eth_account import Account
from datetime import datetime
from web3 import Web3
import asyncio
import os
from .tasks import check_ethereum_address
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from decimal import Decimal, ROUND_DOWN

from channels.layers import get_channel_layer
from django.http import HttpResponse
import requests as request
from .models import (
    paymentHistory,
    paymentRequest,
    USDPaymentRequest
)
from .serializers import (
    paymentHistorySerializer,
    paymentRequestSerializer,
    USDPaymentRequestSerializer
)

# Create your views here.


class paymentHistoryApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, requests, *args, **kwargs) :

        payments = paymentHistory.objects.all()
        serializer = paymentHistorySerializer(payments, many=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response
    
class newPayRequest(APIView):

    def post(self, requests, *args, **kwargs):
       

        #generate a new account dedicated for this specific payment
        account = Account.create()
        private_key = account.key.hex()
        address = account.address
        pendingAmount = requests.data.get("amount")
        destinationAddress = requests.data.get("recipient")
        
        try:
            Decimal(pendingAmount)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        resData = {
            "privateKey": private_key,
            "createdAddress": address,
            "pendingAmount": pendingAmount,
            "destinationAddress": destinationAddress,   #FIXME: need to find a more secure way to do this, but should get the job done for now
            "fullfilled": False,
            "requestDate": datetime.now()
        }

        #launch an asynchronous task that listens for activity on the wallet address created
        #timeout 2 minutes
        #1 api request every 30 seconds
        check_ethereum_address.delay(address, private_key, Decimal(pendingAmount), destinationAddress)

        serializer = paymentRequestSerializer(data=resData)
        if serializer.is_valid():
            serializer.save()
            return Response(resData, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class newPayRequestUSD(APIView):
    def post(self, requests, *args, **kwargs):
        #generate a new account dedicated for this specific payment
        account = Account.create()
        private_key = account.key.hex()
        address = account.address
        pendingAmountUSD = requests.data.get("amount")
        destinationAddress = requests.data.get("recipient")

        try:
            Decimal(pendingAmountUSD)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

        #get ethereum price
        url = "https://min-api.cryptocompare.com/data/price"
        params = {
            "fsym": "USD",      #from currency
            "tsyms": "ETH"      #to currency
        }

        response = request.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            usd_price = data["ETH"]
            print("ETH price in USD:", usd_price)
        else:
            print("Request failed with status code:", response.status_code)

        pendingAmountETH = usd_price * float(pendingAmountUSD)

        pendingAmountETH = Decimal(pendingAmountETH)
        pendingAmountETH = pendingAmountETH.quantize(Decimal('0.0000000001'), rounding=ROUND_DOWN)


        resData = {
            "privateKey": private_key,
            "createdAddress": address,
            "pendingAmountUSD": pendingAmountUSD,
            "pendingAmountETH": pendingAmountETH,
            "ETHprice":usd_price,
            "destinationAddress": destinationAddress,   #FIXME: need to find a more secure way to do this, but should get the job done for now
            "fullfilled": False,
            "requestDate": datetime.now()
        }
    
        #run a celery task to monitor the address
        check_ethereum_address.delay(address, private_key, Decimal(pendingAmountETH), destinationAddress, True)

        #save the data
        serializer = USDPaymentRequestSerializer(data=resData)
        if serializer.is_valid():
            serializer.save()
            return Response(resData, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class testMessage(APIView):
    def post(self, requests, *args, **kwargs):
        addy = requests.data.get("addy")

        print("ADDY: ", addy)

        channel_layer = get_channel_layer()
        notification = {
            'type': 'notify_payment',
            'message': "test message"
        }
        async_to_sync(channel_layer.group_send)(addy, notification)

        return Response({}, status=status.HTTP_200_OK)
    

def send_payment_status_notification(reciepient_address, message):
    print("views method recieved")
    channel_layer = get_channel_layer()
    notification = {
        'type': 'notify_payment',
        'message': message
    }
    async_to_sync(channel_layer.group_send)(reciepient_address, notification)

def index(request):
    context ={

    }

    return render(request, 'index.html', context)


    

#TODO: decide if i want to go through with this funcitonality
class funnelFunds(APIView):
    def get(self, request):
        resData = {
            "status": "success"
        }
        return Response(resData, status=status.HTTP_200_OK)

    
