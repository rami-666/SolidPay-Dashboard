from django.urls import re_path as url
from django.urls import path, include
from solidPayApp.views import (
    paymentHistoryApiView,
    newPayRequest,
    testMessage,
    newPayRequestUSD,
    funnelFunds,
    index
)

urlpatterns = [
    path('viewPaymentHistory', paymentHistoryApiView.as_view()),
    path('payRequest', newPayRequest.as_view(), name='new-pay-request'),
    path('testMessage', testMessage.as_view()),
    path('usdPayRequest', newPayRequestUSD.as_view()),
    path("", index)
]
