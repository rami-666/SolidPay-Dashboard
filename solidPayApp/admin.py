from typing import Dict, Optional
from django.contrib import admin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import (
    paymentHistory,
    paymentRequest,
    nonEmptyWallets,
    USDPaymentRequest
)

# Register your models here.
# admin.site.site_header("SolidPay")

admin.site.register(paymentHistory)
# admin.site.register(paymentRequest)
# admin.site.register(nonEmptyWallets)

@admin.register(paymentRequest)
class paymentRequestAdmin(admin.ModelAdmin):
    list_display = ("createdAddress", "destinationAddress", "pendingAmount", "fullfilled")

@admin.register(USDPaymentRequest)
class paymentRequestAdmin(admin.ModelAdmin):
    list_display = ("createdAddress", "requestDate", "pendingAmountUSD", "pendingAmountETH", "fullfilled")

@admin.register(nonEmptyWallets)
class nonEmptyWalletsAdmin(admin.ModelAdmin):
    list_display = ("address", "balance", "refunded")
    list_filter = ("address", "balance")
    search_fields = ["address", "balance"]


#TODO: add button to funner all resedue funds to a designated wallet
# class nonEmptyWalletsAdmin(admin.ModelAdmin):
#     list_display = ("address", "balance")

#     def change_view(self, request: HttpRequest, object_id: str, form_url: str = ..., extra_context: Dict[str, bool] | None = ...) -> HttpResponse:
#         if extra_context is None:
#             extra_context = {}

#         funnelFundsUrl = reverse('admin:funnelFunds') #TODO: add view url here
#         extra_context['funnelFundsUrl'] = funnelFundsUrl
#         return super().change_view(request, object_id, form_url, extra_context)
    
# admin.site.register(nonEmptyWallets, nonEmptyWalletsAdmin)
