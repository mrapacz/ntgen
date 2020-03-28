from unittest import mock

import pytest
from pyannotate_runtime.collect_types import resolve_type

from ntgen.models import Attribute
from ntgen.models import NT
from ntgen.utils import normalize_field_name


@pytest.fixture()
def sample_person_nt():
    return NT(
        attrs=[
            Attribute(original_name="name", type=str, value="John"),
            Attribute(original_name="age", type=int, value=24),
            Attribute(
                original_name="address",
                type=NT(attrs=[Attribute("city", str, "Warsaw"), Attribute("street", str, "Biała 13")], name="address",),
                value={"city": "Warsaw", "street": "Biała 13"},
            ),
        ],
        name="person",
    )


class TestAttribute:
    @pytest.fixture(
        params=[None, 1, "string", [1, 2, 3], {1: "1"}, pytest.lazy_fixture("sample_person_nt"),]
    )
    def sample_attribute(self, request, sample_field_name):
        return Attribute(
            original_name=sample_field_name,
            type=request.param if isinstance(request.param, NT) else resolve_type(request.param),
            value=request.param,
        )

    def test_repr_field_name(self, sample_attribute):
        with mock.patch("ntgen.models.normalize_field_name", side_effect=normalize_field_name,) as mock_normalize_field_name:
            assert sample_attribute.repr_field_name == normalize_field_name(
                name=sample_attribute.original_name, leading_undescores_prefix=None,
            )
            mock_normalize_field_name.assert_called_once()

    @pytest.mark.parametrize(
        ("sample_attribute", "expected_type_hint"),
        (
            (1, "int"),
            ("string", "str"),
            (None, "None"),
            ({1: "1"}, "Dict[int, str]"),
            (pytest.lazy_fixture("sample_person_nt"), "Person"),
        ),
        indirect=["sample_attribute"],
    )
    def test_repr_type_hint(self, sample_attribute: Attribute, expected_type_hint: str):
        assert sample_attribute.repr_type_hint == expected_type_hint

    @pytest.mark.parametrize(
        ("sample_attribute", "is_user_defined"),
        ((1, False), ("string", False), (None, False), ({1: "1"}, False), (pytest.lazy_fixture("sample_person_nt"), True),),
        indirect=["sample_attribute"],
    )
    def test_is_user_defined(self, sample_attribute: Attribute, is_user_defined: str):
        assert sample_attribute.is_user_defined == is_user_defined


class TestNT:
    def test_attr_views(self, sample_person_nt: NT):
        assert sample_person_nt.builtin_type_attrs == [
            Attribute(original_name="name", type=str, value="John"),
            Attribute(original_name="age", type=int, value=24),
        ]
        assert sample_person_nt.nt_attrs == [
            Attribute(
                original_name="address",
                type=NT(attrs=[Attribute("city", str, "Warsaw"), Attribute("street", str, "Biała 13")], name="address",),
                value={"city": "Warsaw", "street": "Biała 13"},
            )
        ]
