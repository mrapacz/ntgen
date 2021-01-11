import json
from pathlib import Path
from typing import Optional

from tap import Tap as TypedArgumentParser

from ntgen import generate_from_dict


class ArgumentParser(TypedArgumentParser):
    """Generate NamedTuple definitions with typehints based on your data automatically."""

    input: str  # Json file containing an object with the data to analyzed
    out: Optional[str] = None  # Destination file to write the Python code to
    name: Optional[str] = None  # Name of the main NamedTuple, if not passed, it will be inferred from the input filename

    snake_case: bool = True  # Convert the NamedTuple field names to snake_case
    camel_case: bool = True  # Convert the NamedTuple class names to CamelCase
    add_from_dict: bool = False  # Insert generic methods that will allow for parsing of the analyzed data structures
    add_as_dict: bool = False  # Insert generic methods allowing for dumping the nested NamedTuple hierarchy to a dict
    max_level: Optional[int] = None  # Specify the max nesting level of the NamedTuple

    def configure(self) -> None:
        """Make the 'input' argument positional."""
        self.add_argument("input")
        self.add_argument("-s", "--snake-case", action="store_false")
        self.add_argument("-c", "--camel-case", action="store_false")
        self.add_argument("-f", "--add-from-dict", action="store_true")
        self.add_argument("-a", "--add-as-dict", action="store_true")


def main() -> None:
    """Parse arguments and execute ntgen when rune form the command line interface."""
    args = ArgumentParser().parse_args()

    input_file = Path(args.input)
    with input_file.open() as f:
        data = json.load(f)

    name = args.name or input_file.stem

    rendered_nt = generate_from_dict(
        data=data,
        name=name,
        snake_case=args.snake_case,
        camel_case=args.camel_case,
        insert_from_dict=args.add_from_dict,
        insert_as_dict=args.add_as_dict,
        max_level=args.max_level,
    )

    if args.out is None:
        print(rendered_nt)
    else:
        with open(args.out, "w") as f:
            f.write(rendered_nt)
