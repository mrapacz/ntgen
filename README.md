# ntgen
Generate NamedTuple definitions with typehints based on your data automatically.
If you've ever felt like preparing NamedTuple skeletons for any json data you're dealing with is tedious and could be
automated, well, this is the tool that automates the process.

## Usage
Let's say you want to prepare a NamedTuple definition for the following json object:
```bash
$ cat apartment.json
{
    "id": "1234-1234",
    "type": "living",
    "isAvailable": true,
    "countryCode": "DE",
    "address": {
        "borough": "Dulsberg",
        "city": "Hamburg",
        "houseNumber": "2",
        "latitude": 53.587485,
        "longitude": 10.063215,
        "postalCode": "22049",
        "streetName": "Nordschleswiger Strasse",
        "area": "Hamburg"
    },
    "_attachments": "attachments/",
    "_ts": 15828103462
}%
```

All you need to do is run the following command:
```bash
$ ntgen apartment.json
class Address(NamedTuple):
    borough: str
    city: str
    house_number: str
    latitude: float
    longitude: float
    postal_code: str
    street_name: str
    area: str



class Apartment(NamedTuple):
    id: str
    type: str
    is_available: bool
    country_code: str
    address: Address
    attachments: str
    ts: int

```
The output will be directed to stdout by default - you may also redirect it to a file to bootstrap a Python module with
the class definitions.

## Runtime configuration

To find out about all of the runtime configuration options, run:
```bash
$ ntgen --help
usage: ntgen [--out OUT] [--name NAME] [-s] [-c] [--insert_constructors] [--insert_as_dict] [--max_level MAX_LEVEL] [-h] input

positional arguments:
  input                 (str, default=None) Json file containing an object with the data to analyzed

optional arguments:
  --out OUT             (Union[str, NoneType], default=None) Destination file to write the Python code to
  --name NAME           (str, default=NTGenTuple) Name of the main NamedTuple
  -s, --snake-case      (bool, default=False) Convert the NamedTuple field names to snake_case
  -c, --camel-case      (bool, default=True) Convert the NamedTuple class names to CamelCase
  --insert_constructors
                        (bool, default=True) Insert generic methods that will allow for parsing of the analyzed data structures
  --insert_as_dict      (bool, default=True) Insert generic methods allowing for dumping the nested NamedTuple hierarchy to a dict
  --max_level MAX_LEVEL
                        (Union[int, NoneType], default=None) Specify the max nesting level of the NamedTuple
  -h, --help            show this help message and exit
```

## Other invocation options
You can also use the library from the Python context:
```python
>>> from ntgen import generate_from_dict
>>> data = {'name': 'John Wick', 'profession': 'assassin', 'age': 34}
>>> print(generate_from_dict(data=data, name="Character"))
class Character(NamedTuple):
    name: str
    profession: str
    age: int

```
## Installation
You'll need to be running Python >= 3.7.
```bash
pip install ntgen
```
Verify that the latest package version was installed correctly:
```python
>>> import ntgen
>>> ntgen.__version__
'0.1.0'

```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Author
Maciej Rapacz
