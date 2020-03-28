from unittest import mock

import pytest

from ntgen.utils import convert_to_snake_case
from ntgen.utils import indent_statement
from ntgen.utils import normalize_class_name
from ntgen.utils import normalize_field_name
from ntgen.utils import replace_leading_underscores


class TestUtils:
    @pytest.fixture(params=[None, "sample_prefix", "another"])
    def sample_prefix(self, request):
        return request.param

    @pytest.fixture(params=["SamplePascalName123", "sample_snake_case_name_123", "sample-kebab-case-123"])
    def sample_name(self, request):
        return request.param

    @pytest.mark.parametrize(
        ("indent", "statement", "expected_string"),
        (
            (0, "some_statement", "some_statement"),
            (1, "some_statement", "    some_statement"),
            (2, "some_statement", "        some_statement"),
            (0, "def test():", "def test():"),
            (1, "def test():", "    def test():"),
            (2, "def test():", "        def test():"),
        ),
    )
    def test_indent_statement(self, indent, statement, expected_string):
        assert indent_statement(indent=indent, statement=statement) == expected_string

    def test_normalize_field_name(self, sample_name, sample_prefix):
        with mock.patch("ntgen.utils.convert_to_snake_case",) as mock_convert_to_snake_case, mock.patch(
            "ntgen.utils.replace_leading_underscores",
        ) as mock_replace_leading_underscores:
            normalize_field_name(name=sample_name, leading_undescores_prefix=sample_prefix)

            mock_convert_to_snake_case.assert_called_once()
            mock_replace_leading_underscores.assert_called_once()

    @pytest.mark.parametrize(
        ("name", "expected_output"),
        (
            ("SamplePascalName123", "sample_pascal_name123"),
            ("sample_snake_case_name_123", "sample_snake_case_name_123"),
            ("sample-kebab-case-123", "sample_kebab_case_123"),
        ),
    )
    def test_convert_to_snake_case(self, name, expected_output):
        assert convert_to_snake_case(name) == expected_output

    @pytest.mark.parametrize(
        ("name", "expected_output"),
        (
            ("SamplePascalName123", "SamplePascalName123"),
            ("sample_snake_case_name_123", "SampleSnakeCaseName123"),
            ("sample-kebab-case-123", "SampleKebabCase123"),
        ),
    )
    def test_normalize_class_name(self, name, expected_output):
        assert normalize_class_name(name) == expected_output

    @pytest.mark.parametrize(
        ("name", "prefix", "expected_output"),
        (
            ("normalized_name", None, "normalized_name"),
            ("normalized_name", "some_prefix", "normalized_name"),
            ("_incorrect_name", None, "incorrect_name"),
            ("__incorrect_name", None, "incorrect_name"),
            ("__incorrect_name", "some_prefix", "some_prefix_incorrect_name"),
            ("____incorrect_name", "some_prefix", "some_prefix_incorrect_name"),
        ),
    )
    def test_replace_leading_underscores(self, name, prefix, expected_output):
        assert replace_leading_underscores(name, prefix=prefix) == expected_output
