import re
from typing import Optional


def normalize_field_name(name: str, leading_undescores_prefix: Optional[str] = None) -> str:
    """
    Normalize a string to take a Pythonic form.

    Normalize a string to take a Pythonic form by:
    - replacing leading underscores with a given (optional) prefix
    - converting the name so snake_case
    """
    return convert_to_snake_case(replace_leading_underscores(name, prefix=leading_undescores_prefix))


def convert_to_snake_case(name: str) -> str:
    """
    Convert a given string to snake_case.

    Converts a given string to snake_case from camel case or kebab case
    >>> normalize_field_name('SomeCamelCase')
    'some_camel_case'
    >>> normalize_field_name('sample-kebab-case')
    'sample_kebab_case'
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).replace("-", "_").lower()


def normalize_class_name(name: str) -> str:
    """
    Normalize class name by converting it to PascalCase.

    >>> normalize_class_name('some_hyphen_case')
    'SomeHyphenCase'
    """
    if re.match(r"(?:[A-Z][a-z]+)+", name):
        return name

    return "".join([fragment.capitalize() for fragment in normalize_field_name(name).split("_")])


def replace_leading_underscores(name: str, prefix=None) -> str:
    """
    Replace leading underscores with a given prefix.

    Replaces leading underscores with a given prefix. If no prefix is specified, the leading underscores are removed.
    >>> replace_leading_underscores('_private_field')
    'private_field'
    >>> replace_leading_underscores('__private_field', prefix='dunder')
    'dunder_private_field'
    """
    return re.sub(r"^_+", f"{prefix}_" if prefix else "", name)


def indent_statement(indent: int, statement: str) -> str:
    """
    Indents the given string by a specified number of indents.

    Indents the given string by a specified number of indents, e.g. indenting by 1 will preprend the string
    with 4 space characters:
    >>> indent_statement(0, 'x = 3')
    'x = 3'
    >>> indent_statement(1, 'x = 3')
    '    x = 3'
    """
    return " " * 4 * indent + statement
