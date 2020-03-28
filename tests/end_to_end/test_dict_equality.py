import importlib
from pathlib import Path
from shutil import copyfile

from ntgen import generate_from_dict
from ntgen.utils import normalize_class_name
from tests.conftest import normalize_keys


class TestGeneratedDictionaryIsEquivalentWithOriginal:
    module_template_path = Path("tests") / "end_to_end" / "module_template.py"

    def test_interpreted_dict_exports_to_the_same_as_input(self, tmp_module, sample_dict):
        example_dict_object, submodule_name = sample_dict
        module_path = copyfile(self.module_template_path, tmp_module / f"{submodule_name}.py")

        main_object_name = normalize_class_name(submodule_name)
        nt_code = generate_from_dict(data=example_dict_object, name=main_object_name, insert_as_dict=True, insert_from_dict=True)

        with module_path.open("a") as f:
            f.write(nt_code)

        test_module_obj = importlib.import_module(str(tmp_module / submodule_name).replace("/", "."))
        nt_class = getattr(test_module_obj, main_object_name)

        nt_object = nt_class.from_dict(example_dict_object)
        nt_exported_to_dict = nt_object.as_dict()

        assert normalize_keys(nt_exported_to_dict) == normalize_keys(example_dict_object)
