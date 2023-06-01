from celery import shared_task
import time
from web3 import Web3
import os
from eth_account import Account
from decimal import Decimal, ROUND_DOWN
from asgiref.sync import async_to_sync, sync_to_async

from .models import (
    paymentRequest,
    USDPaymentRequest
)
from .serializers import (
    paymentRequestSerializer,
    nonEmptyWalletsSerializer
)
from .consumers import (
    PaymentStatusConsumer
)

#TODO: CHECK IF IT IS MORE SECURE TO USE channel_name INSTEAD OF GROUP NAME
def send_notification(request, address, channel_name, message):
    print("CHANNEL NAME: ", channel_name)

    from solidPayApp.views import send_payment_status_notification
    
    send_payment_status_notification(address, message)

@shared_task
def check_ethereum_address(address, privKey, expectedDeposit, recipient_address, isUSD):
    print('RECIEVED ADDRESS: ', address)
    infuraId = os.environ.get("INFURA_ID")
    expired = False
    zeroBalance = True
    expCount = 0

    decimal_expectedDeposit = Decimal(expectedDeposit)
    limited_decimal_expectedDeposit = decimal_expectedDeposit.quantize(Decimal('0.0000000001'), rounding=ROUND_DOWN)
    
    web3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/" + infuraId))


    while True:
        expCount += 1
        balance = web3.from_wei(web3.eth.get_balance(address), 'ether')
        if(balance > 0):  
            print("new transaction detected")
            zeroBalance = False
            if(balance >= limited_decimal_expectedDeposit):
                print("balance is sufficient")
                break

        if expCount >= 4:       #TODO: edit exp count depending on expiry time decision
            print("no transactions detected for 2 minutes")
            expired = True 
            break

        time.sleep(30)

    expCount = 0

    print("getting channel name...")

    while True:
        expCount += 1

        if not isUSD:
            channelPayRequest = paymentRequest.objects.get(privateKey=privKey)
        else:
            channelPayRequest = USDPaymentRequest.objects.get(privateKey=privKey)
        
        if channelPayRequest is not None and channelPayRequest.channel != "":
            print("channel name is: ", channelPayRequest.channel)
            channel_name = channelPayRequest.channel
            break
        elif expCount >= 3:
            break

        time.sleep(30)

    if not expired:
        print(f"Sender balance: {balance} ETH")

        gas = web3.to_wei(50, "gwei")
        

        # Create a transaction
        transaction = {
            "to": recipient_address,
            "value": web3.to_wei(balance, 'ether') ,  # Set the value to the entire balance
            "gas": "21000",  # Gas limit
            "gasPrice": gas,  # Gas price (in Wei)
            "nonce": web3.eth.get_transaction_count(address),  # Nonce value
        }

        gas_limit = web3.eth.estimate_gas(transaction)
        transaction["gas"] = gas_limit
        transaction["value"] = web3.to_wei(balance, 'ether') - (gas_limit * gas)

        # Sign the transaction
        signed_transaction = Account.sign_transaction(transaction, privKey)

        # Send the transaction
        transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        # Wait for the transaction to be mined
        receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

        # Check if the transaction was successful
        if receipt.status == 1:
            print("Transaction successful!")
            print("Transaction hash:", transaction_hash.hex())
            print("Gas used:", receipt.gasUsed)


            if not isUSD:
                payRequest= paymentRequest.objects.get(privateKey=privKey)

            else:
                payRequest = USDPaymentRequest.objects.get(privateKey=privKey)

            payRequest.fullfilled = True
            payRequest.save()

            send_notification(None, address,channel_name, "SUCCESSFUL PAYMENT")

        else:
            print("Transaction failed.")

    elif (expired and not zeroBalance):
        print("wallet is not empty!")
        print("saving details of non-empty wallet")
        print(f"Sender balance: {balance} ETH")
        send_notification(None, address,channel_name, "Partial payment made within the time limit, contact support for refund.")

        resData = {
            "privateKey": privKey,
            "address": address,
            "balance": balance
        }

        serializer = nonEmptyWalletsSerializer(data=resData)
        if serializer.is_valid():
            serializer.save()
            print("wallet saved")
        else:
            raise Exception("ERROR SAVING NON-EMPTY WALLET")
        
    if expired:
        send_notification(None, address, channel_name, "FAILED TO MAKE PAYMENT WITHIN TIME LIMIT")
        
    
    print("Shutting down thread...")

