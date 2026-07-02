import importlib.util
import unittest
from pathlib import Path


class ImportPathTests(unittest.TestCase):
    def test_import_example_module_with_project_src_path(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        example_path = repo_root / "examples" / "test_fase1.py"
        spec = importlib.util.spec_from_file_location("test_fase1", example_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.assertTrue(callable(getattr(module, "main", None)))


if __name__ == "__main__":
    unittest.main()
