from datetime import timedelta

from drf_spectacular.utils import OpenApiResponse

DEMO_SIZE = 7

DELTA_FRESH = timedelta(hours=1000)

RESPONSE_STR = OpenApiResponse(
    response={
        'type': 'string',
    }
)
RESPONSE_LIST_STR = OpenApiResponse(
    response={
        'type': 'array',
        'items': {'type': 'string'}
    }
)
RESPONSE_SUMMARY = OpenApiResponse(
    response={
        'type': 'object',
        'properties': {
            'exchanges': {'type': 'integer'},
            'symbols': {'type': 'integer'},
            'profit_deals': {'type': 'integer'},
            'uptime': {'type': 'number', 'format': 'float'},
        }
    }
)
