from ntgen.config import Config
from ntgen.models import Attribute
from ntgen.models import NT
from ntgen.utils import indent_statement


def _render_subtuples(nt_definition: NT, config: Config) -> str:
    return "".join(
        _render_nt_definition(sub_tuple.type, config=config) for sub_tuple in nt_definition.attrs if isinstance(sub_tuple.type, NT)
    )


def _render_signature(nt_definition: NT) -> str:
    return f"class {nt_definition}(NamedTuple):\n"


def _render_attribute(attr: Attribute) -> str:
    return f"{attr.repr_field_name}: {attr.repr_type_hint}\n"


def _render_attributes(nt_definition: NT) -> str:
    return "".join(indent_statement(indent=1, statement=_render_attribute(attr)) for attr in nt_definition.attrs)


def _render_constructor(nt_definition: NT) -> str:
    param_assignments = []
    for attr in nt_definition.builtin_type_attrs:
        param_assignments.append(f"{attr.repr_field_name}=data['{attr.original_name}'],")

    for attr in nt_definition.nt_attrs:
        param_assignments.append(f"{attr.repr_field_name}={attr.type}.from_dict(data['{attr.original_name}']),")

    indents_statements = (
        (1, "@classmethod"),
        (1, f"def from_dict(cls, data: Dict) -> {nt_definition}:"),
        (2, f"return {nt_definition}("),
        *[(3, param) for param in param_assignments],
        (2, ")"),
    )

    return "\n".join(indent_statement(indent, statement) for indent, statement in indents_statements) + "\n\n"


def _render_as_dict_method() -> str:
    indents_statements = (
        (1, f"def as_dict(self) -> Dict:"),
        (2, f"return {{"),
        (3, f'name: (value.as_dict() if hasattr(value, "as_dict") else value)'),
        (3, f"for name, value in self._asdict().items()"),
        (2, f"}}"),
    )

    return "\n".join(indent_statement(indent, statement) for indent, statement in indents_statements) + "\n\n"


def _render_nt_definition(nt_definition: NT, config: Config) -> str:
    return "".join(
        (
            _render_subtuples(nt_definition, config=config),
            "\n",
            _render_signature(nt_definition),
            _render_attributes(nt_definition),
            "\n",
            _render_constructor(nt_definition) if config.insert_from_dict else "",
            _render_as_dict_method() if config.insert_as_dict else "",
        ),
    )


def render_nt_definition(nt_definition: NT, config: Config) -> str:
    """
    Render a NamedTuple type class definition based on a given NT object.

    :param nt_definition: NT object
    :param config: Config object
    :return: string containing valid Python code declaring a NamedTuple
    """
    return _render_nt_definition(nt_definition=nt_definition, config=config).lstrip().rstrip()
