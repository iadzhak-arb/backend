from contextlib import asynccontextmanager

from django.conf import settings

from faststream.rabbit import RabbitBroker, Channel

from orderbooks.consumers import router as orderbooks_router

channel = Channel(prefetch_count=1)
broker = RabbitBroker(settings.RMQ_URL, default_channel=channel)

broker.include_router(orderbooks_router)


@asynccontextmanager
async def broker_lifespan(app):
    await broker.start()
    try:
        yield
    finally:
        await broker.stop()
