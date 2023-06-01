"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from django.urls import re_path

from solidPayApp.consumers import (
    PaymentStatusConsumer,
    USDPaymentStatusConsumer
)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":  URLRouter([
                re_path(r"^ws/payment-status/(?P<address>\w+)/$", PaymentStatusConsumer.as_asgi()),
                re_path(r"^ws/payment-status/usd/(?P<address>\w+)/$", USDPaymentStatusConsumer.as_asgi()),
            ])
            #FIXME: check why authmiddlewarestack and allowedhostsoriginvalidator are not working
        # AuthMiddlewareStack(
           
        # )
    
})
