# celery.py

import os
from django.conf import settings
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Create a Celery instance
app = Celery('core')

# Configure the Celery instance
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
