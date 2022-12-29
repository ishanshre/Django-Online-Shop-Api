"""
Configuration for celery
"""

import os
from celery import Celery

# refrence our project settings to DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'core.settings')

# create a Celery instance with a project name
celery = Celery('core')

# set config_from_object to settings with <module name>:settings i.e. django.conf:settings
celery.config_from_object('django.conf:settings', namespace="CELERY")

# tell celery to auto discover the task
celery.autodiscover_tasks()

"""Must load or import this file in __init__ file otherwise python will not execute this code"""

