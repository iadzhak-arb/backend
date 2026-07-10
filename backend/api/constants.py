from datetime import timedelta

from drf_spectacular.utils import OpenApiResponse

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
