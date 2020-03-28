from __future__ import annotations

from typing import NamedTuple
from typing import Optional


class Config(NamedTuple):
    """NamedTuple class for storage of named tuple rendering options."""

    snake_case: bool = True
    camel_case: bool = True
    insert_from_dict: bool = False
    insert_as_dict: bool = False
    max_level: Optional[int] = None
