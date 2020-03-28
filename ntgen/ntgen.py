from typing import Dict
from typing import Optional

from ntgen.config import Config
from ntgen.exception import InputDataStructureIsNotADict
from ntgen.models import NT
from ntgen.render import render_nt_definition


def generate_from_dict(
    data: Dict,
    name="NTGenNamedTuple",
    snake_case: bool = True,
    camel_case: bool = True,
    insert_as_dict: bool = False,
    insert_from_dict: bool = False,
    max_level: Optional[int] = None,
) -> str:
    """
    Generate a string containing NamedTuple definition based on the given dictionary.

    :param data: dictionary to be rendered as a NamedTuple
    :param name: name for the NamedTuple
    :param snake_case: true if the NamedTuple field names should be transformed to snake_case
    :param camel_case: true if the NamedTuple class names should be transformed to CamelCase
    :param insert_as_dict: insert methods allowing for dumping nested structures to dictionaries
    :param insert_from_dict: insert generic constructors that will allow for parsing the analyzed data
    :param max_level: set the depth level for sub-tuple generation
    :return: string - valid Python code containing the definition of a NamedTuple based on the provided data structure
    """
    config = Config(
        snake_case=snake_case,
        camel_case=camel_case,
        insert_from_dict=insert_from_dict,
        insert_as_dict=insert_as_dict,
        max_level=max_level,
    )

    nt = NT.parse_dict(data=data, name=name, config=config, level=1)
    if nt is None:
        raise InputDataStructureIsNotADict(f"The input data structure was not valid. Should be a non-empty dict, was: {data}")
    return render_nt_definition(nt, config)
