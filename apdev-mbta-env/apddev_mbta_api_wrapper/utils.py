from __future__ import annotations

import os

MBTA_API_DOMAIN = 'https://api-v3.mbta.com'

def getDefaultHeaders():
    api_key = os.getenv('MBTA_API_KEY')
    return {
        'accept': 'application/vnd.api+json',
        'x-api-key': api_key
    }
