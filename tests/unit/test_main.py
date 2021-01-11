import argparse
from unittest import mock
from unittest.mock import mock_open

import pytest

import ntgen.main as test_module
from ntgen.main import main


class TestMain:
    @pytest.fixture(autouse=True, params=[{}])
    def patch_json_file_contents(self, request):
        with mock.patch("ntgen.main.Path.open"), mock.patch(
            "ntgen.main.json.load",
            return_value=request.param,
        ):
            yield

    @pytest.fixture(autouse=True)
    def patch_open(self):
        with mock.patch(
            "ntgen.main.open",
            mock_open(),
        ) as patch_write:
            yield patch_write

    @pytest.fixture(autouse=True)
    def patch_generate_from_dict(self):
        with mock.patch.object(test_module, "generate_from_dict", return_value="namedtuple") as patch_generate:
            yield patch_generate

    @pytest.fixture
    def patch_parsed_args(self, request):
        defaults = {
            "input": "input.json",
            "out": None,
            "name": None,
            "snake_case": True,
            "camel_case": True,
            "add_from_dict": False,
            "add_as_dict": False,
            "max_level": None,
        }
        with mock.patch(
            "ntgen.main.ArgumentParser.parse_args",
            return_value=argparse.Namespace(**{**defaults, **request.param}),
        ):
            yield

    @pytest.mark.parametrize(
        argnames=["patch_parsed_args", "patch_json_file_contents", "expected_kwargs"],
        argvalues=[
            pytest.param(
                {"input": "apartment.json", "name": None},
                {},
                dict(
                    data={},
                    name="apartment",
                    snake_case=True,
                    camel_case=True,
                    insert_from_dict=False,
                    insert_as_dict=False,
                    max_level=None,
                ),
                id="default values, infer the name from filename",
            ),
            pytest.param(
                {"input": "apartment.json", "name": "Building"},
                {},
                dict(
                    data={},
                    name="Building",
                    snake_case=True,
                    camel_case=True,
                    insert_from_dict=False,
                    insert_as_dict=False,
                    max_level=None,
                ),
                id="override name param with Input",
            ),
            pytest.param(
                {},
                {"some_key": 42},
                dict(
                    data={"some_key": 42},
                    name="input",
                    snake_case=True,
                    camel_case=True,
                    insert_from_dict=False,
                    insert_as_dict=False,
                    max_level=None,
                ),
                id="passes the loaded json object",
            ),
        ],
        indirect=["patch_parsed_args", "patch_json_file_contents"],
    )
    def test_main_passes_args_to_generate_correctly(
        self,
        patch_generate_from_dict,
        patch_parsed_args,
        patch_json_file_contents,
        expected_kwargs,
    ):
        main()
        patch_generate_from_dict.assert_called_once_with(**expected_kwargs)

    @pytest.mark.parametrize(
        argnames=("patch_parsed_args", "expected_stdout", "expected_write_call_value"),
        argvalues=(
            pytest.param({}, "namedtuple\n", None, id="Writes to stdout by default"),
            pytest.param({"out": "filename.py"}, "", "namedtuple", id="Writes to file if called with --out flag"),
        ),
        indirect=["patch_parsed_args"],
    )
    def test_main_respects_out_flag(self, patch_open, capsys, patch_parsed_args, expected_stdout, expected_write_call_value):
        main()

        assert capsys.readouterr() == (expected_stdout, "")
        if expected_write_call_value:
            patch_open.assert_called_once_with("filename.py", "w")
            patch_open().write.assert_called_once_with("namedtuple")
        else:
            patch_open.assert_not_called()
