from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    paymentHistory,
    paymentRequest,
    nonEmptyWallets,
    USDPaymentRequest
)

class paymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = paymentHistory
        fields = "__all__"

class paymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = paymentRequest
        fields = "__all__"

class nonEmptyWalletsSerializer(serializers.ModelSerializer):
    class Meta:
        model = nonEmptyWallets
        fields = "__all__"

class USDPaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = USDPaymentRequest
        fields = "__all__"