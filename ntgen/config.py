import sys
from typing import NamedTuple
from typing import Optional

IS_PY_37_COMPATIBLE = sys.version_info.major == 3 and sys.version_info.minor >= 7


class Config(NamedTuple):
    """NamedTuple class for storage of named tuple rendering options."""

    snake_case: bool = True
    camel_case: bool = True
    insert_from_dict: bool = False
    insert_as_dict: bool = False
    max_level: Optional[int] = None
