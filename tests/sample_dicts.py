"""A module for storing larger test data in Python format."""
from typing import Any
from typing import Dict

APARTMENT_DICT: Dict[str, Any] = {
    "id": "1234-1234",
    "type": "living",
    "countryCode": "DE",
    "availableUntilDate": None,
    "availableFromDate": "2018-05-16T00:00:00Z",
    "availableFromNowOn": False,
    "publishedFromDate": None,
    "address": {
        "borough": "Dulsberg",
        "city": "Hamburg",
        "houseNumber": "2",
        "latitude": 53.587485,
        "longitude": 10.063215,
        "postalCode": "22049",
        "streetName": "Nordschleswiger Straße",
        "area": "Hamburg",
    },
    "_attachments": "attachments/",
    "_ts": 15828103462,
}

EX_DICT: Dict[str, Any] = {
    "butter": 3,
    "name": "Thomas",
    "volume": 3.14,
    "items": [1, 2, 3],
    "obligatory_items": (1, 2, 3),
}
