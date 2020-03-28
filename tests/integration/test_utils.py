import pytest

from ntgen.utils import normalize_field_name


@pytest.mark.parametrize(
    ("name", "prefix", "expected_field_name"),
    (("field_name", None, "field_name"), ("__FieldName", None, "field_name"), ("___FieldName", "prefix", "prefix__field_name"),),
)
def test_normalize_field_name(name, prefix, expected_field_name):
    assert normalize_field_name(name=name, leading_undescores_prefix=prefix) == expected_field_name
