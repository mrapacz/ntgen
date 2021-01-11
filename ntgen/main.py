import argparse
import json
from pathlib import Path

from ntgen import generate_from_dict


def parse_args() -> argparse.Namespace:
    """Define CLI args for the ntgen entrypoint."""
    parser = argparse.ArgumentParser("ntgen")

    parser.add_argument("input", help="JSON file containing an object with the data to analyzed")
    parser.add_argument("-o", "--out")
    parser.add_argument("-s", "--snake-case", action="store_false", help="Convert the NamedTuple field names to snake_case")
    parser.add_argument("-c", "--camel-case", action="store_false", help="Convert the NamedTuple class names to CamelCase")
    parser.add_argument(
        "-f",
        "--add-from-dict",
        action="store_true",
        help="Insert generic methods that will allow for parsing of the analyzed data structures",
    )
    parser.add_argument(
        "-a",
        "--add-as-dict",
        action="store_true",
        help="Insert generic methods allowing for dumping the nested NamedTuple hierarchy to a dict",
    )

    parser.add_argument(
        "-n",
        "--name",
        default=None,
        help="Name of the main NamedTuple, if not passed, it will be inferred from the input filename",
    )
    parser.add_argument("--max-level", default=None, type=int, help="Specify the max nesting level of the NamedTuple")

    return parser.parse_args()


def main() -> None:
    """Parse arguments and execute ntgen when rune form the command line interface."""
    args = parse_args()

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
