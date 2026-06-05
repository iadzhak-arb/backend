import os

from django.core.asgi import get_asgi_application
from starlette.applications import Starlette
from starlette.routing import Mount

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django_asgi = get_asgi_application()

from .broker import broker_lifespan

application = Starlette(
    routes=(
        Mount('/', django_asgi),
    ),
    lifespan=broker_lifespan
)
