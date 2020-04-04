"""Test API exposed by the package."""
import pytest

from ntgen import generate_from_dict
from ntgen.exception import InputDataStructureIsNotADict


class TestGenerateFromDict:
    @pytest.mark.parametrize(
        argnames="sample_non_dict_structure",
        argvalues=[[1, 2, 3], "something", 1, 1.2, (1, 2, 3)],
        ids=["list", "string", "int", "float", "tuple"],
    )
    def test_generate_from_dict_raises_when_not_a_dict(self, sample_non_dict_structure):
        with pytest.raises(InputDataStructureIsNotADict):
            generate_from_dict(data=sample_non_dict_structure)
