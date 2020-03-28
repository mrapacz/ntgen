import json
from typing import Optional

from tap import Tap as TypedArgumentParser

from ntgen import generate_from_dict


class ArgumentParser(TypedArgumentParser):
    """Generate NamedTuple definitions with typehints based on your data automatically."""

    input: str  # Json file containing an object with the data to analyzed
    out: Optional[str] = None  # Destination file to write the Python code to
    name: str = "NTGenTuple"  # Name of the main NamedTuple

    snake_case: bool = True  # Convert the NamedTuple field names to snake_case
    camel_case: bool = True  # Convert the NamedTuple class names to CamelCase
    constructors: bool = False  # Insert generic methods that will allow for parsing of the analyzed data structures
    as_dict: bool = False  # Insert generic methods allowing for dumping the nested NamedTuple hierarchy to a dict
    max_level: Optional[int] = None  # Specify the max nesting level of the NamedTuple

    def add_arguments(self):
        """Make the 'input' argument positional."""
        self.add_argument("input")
        self.add_argument("-s", "--snake-case", action="store_false")
        self.add_argument("-c", "--camel-case", action="store_false")
        self.add_argument("-f", "--constructors", action="store_true")
        self.add_argument("-t", "--as-dict", action="store_true")


def main() -> None:
    """Parse arguments and execute ntgen when rune form the command line interface."""
    args = ArgumentParser().parse_args()

    with open(args.input) as f:
        data = json.load(f)

    rendered_nt = generate_from_dict(
        data=data,
        name=args.name,
        snake_case=args.snake_case,
        camel_case=args.camel_case,
        insert_from_dict=args.constructors,
        insert_as_dict=args.as_dict,
        max_level=args.max_level,
    )

    if args.out is None:
        print(rendered_nt)
    else:
        with open(args.out, "w") as f:
            f.write(rendered_nt)
