from datetime import timedelta

DELTA_FRESH = timedelta(hours=1000)
RESPONSE_LIST_STR = {
    200: {
        'description': 'Список токенов',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'array',
                    'items': {'type': 'string'}
                }
            }
        }
    }
}
