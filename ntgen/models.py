from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Type
from typing import Union

from pyannotate_runtime.collect_types import InternalType
from pyannotate_runtime.collect_types import resolve_type

from ntgen.config import Config
from ntgen.utils import normalize_class_name
from ntgen.utils import normalize_field_name


class NT(NamedTuple):
    """
    Contains meta data of a future NamedTuple definition.

    The NT class contains meta data which may be rendered as a single or multiple NamedTuple definitions. An instance of the class
    may be created using a direct class initialization or by parsing a dictionary using the parse_dict class method.
    """

    attrs: List[Attribute]  # type: ignore
    name: str

    def __repr__(self) -> str:
        """Format the structure name to be a Pythonic class identifier."""
        return normalize_class_name(self.name)

    @property
    def nt_attrs(self) -> List[Attribute]:
        """Return a list of all the 'user defined' type attributes of the data structure."""
        return [attr for attr in self.attrs if attr.is_user_defined]

    @property
    def builtin_type_attrs(self) -> List[Attribute]:
        """Return a list of all the builtin type attributes in the data structure."""
        return [attr for attr in self.attrs if not attr.is_user_defined]

    @classmethod
    def parse_dict(cls, data: Dict, name: str, config: Config, level: int = 0) -> Optional[NT]:
        """
        Parse a given dictionary to identify future NamedTuple metadata.

        :param data: dictionary to be parsed
        :param name: name of the future NamedTuple
        :param config: Config instance
        :param level: prevents the method from creating too deeply-nested NamedTuple definitions
        :return: An instance of the NT class if it's non-empty (i.e. it contains any attributes)
        """
        if not isinstance(data, dict):
            return None

        should_nest = config.max_level is None or level < config.max_level

        attrs = []
        for attr_name, attr_value in data.items():
            nt = NT.parse_dict(data=attr_value, name=attr_name, level=level + 1, config=config)
            attribute_type = nt if nt and should_nest else resolve_type(attr_value)

            attrs.append(Attribute(original_name=attr_name, type=attribute_type, value=attr_value))

        return NT(attrs=attrs, name=name) if attrs else None


class Attribute(NamedTuple):
    """
    A class representing metadata of a future NamedTuple definition attribute.

    The class stores metadata about a NamedTuple attribute, namely:
    - the attribute name
    - inferred attribute type
    - original value of the attribute used to infer the type

    The attribute type may be one of:
    - NoneType
    - built-in types which cannot be parameterized such as str, int, float, etc.
    - pyannotate type in case if the attribute will be rendered as a built-in parameterizable type, e.g. Dict[T,T], Tuple[T, int]
    - NT object if the attribute will be rendered as a NamedTuple definition
    """

    original_name: str
    type: Union[InternalType, NT, Type[None]]
    value: Any

    @property
    def repr_field_name(self) -> str:
        """Return the attribute name normalized to be a valid pythonic NamedTuple field name."""
        return normalize_field_name(name=self.original_name, leading_undescores_prefix=None)

    @property
    def repr_type_hint(self) -> str:
        """Return a string representing a type hint for the attribute."""
        if self.type is type(None):  # noqa: E721 # there's no other way to check for NoneType
            return "None"

        if isinstance(self.type, type):
            return self.type.__name__

        return repr(self.type)

    @property
    def is_user_defined(self) -> bool:
        """Return True if the attribute will be rendered as a user defined type (namely a NamedTuple)."""
        return isinstance(self.type, NT)
