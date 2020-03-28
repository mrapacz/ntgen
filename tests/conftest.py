from typing import Dict

import pytest

from ntgen.utils import normalize_field_name
from ntgen.utils import replace_leading_underscores
from tests.sample_dicts import APARTMENT_DICT
from tests.sample_dicts import EX_DICT


@pytest.fixture(params=[(APARTMENT_DICT, "akelius_dict"), (EX_DICT, "example_dict")])
def sample_dict(request):
    return request.param


@pytest.fixture(params=["sample_name", "__sample_name", "SampleName", "sample-name"])
def sample_field_name(request):
    return request.param


def normalize_keys(data: Dict) -> Dict:
    assert isinstance(data, dict)

    normalized_dict = {}
    for key, value in data.items():
        normalized_key = replace_leading_underscores(normalize_field_name(key))
        normalized_dict[normalized_key] = normalize_keys(value) if isinstance(value, dict) else value
    return normalized_dict
