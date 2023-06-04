from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class paymentHistory(models.Model):
    sender = models.CharField(max_length=500)
    amount = models.DecimalField(decimal_places=10, max_digits=30)
    date = models.DateField()

    def __str__(self):
        return self.sender + ": " + self.amount + " ETH"
    
class paymentRequest(models.Model):
    privateKey = models.CharField(max_length=1000)
    createdAddress = models.CharField(max_length=500)
    pendingAmount = models.DecimalField(decimal_places=10, max_digits=30)
    destinationAddress = models.CharField(max_length=500)
    channel = models.CharField(max_length=300, default="")
    fullfilled = models.BooleanField(default=False)
    requestDate = models.DateTimeField()

    def __str__(self):
        return self.createdAddress + " to " + self.destinationAddress + " (" + str(self.pendingAmount) + ")"

class USDPaymentRequest(models.Model):
    privateKey = models.CharField(max_length=1000)
    createdAddress = models.CharField(max_length=500)
    pendingAmountUSD = models.DecimalField(decimal_places=10, max_digits=30)
    pendingAmountETH = models.DecimalField(decimal_places=10, max_digits=30)
    ETHprice = models.DecimalField(decimal_places=10, max_digits=10)
    destinationAddress = models.CharField(max_length=500)
    channel = models.CharField(max_length=300, default="")
    fullfilled = models.BooleanField(default=False)
    requestDate = models.DateTimeField()

    def __str__(self):
        return self.createdAddress + " to " + self.destinationAddress + " (" + str(self.pendingAmountUSD) + ")"
    
class nonEmptyWallets(models.Model):
    privateKey = models.CharField(max_length=1000, primary_key=True)
    address = models.CharField(max_length=500)
    balance = models.DecimalField(max_digits=30, decimal_places=10)
    refunded = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.address + " : " + str(self.balance) + " ETH"
