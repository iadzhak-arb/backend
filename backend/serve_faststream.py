import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from faststream import FastStream
from backend.broker import broker

app = FastStream(broker)
