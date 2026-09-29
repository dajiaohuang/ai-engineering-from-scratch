from __future__ import annotations

import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path


LESSON = Path(__file__).resolve().parents[2]


def load_generator():
    source = LESSON / "code" / "main.py"
    spec = importlib.util.spec_from_file_location("workbench_generator", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load generator from {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GeneratorEncodingTests(unittest.TestCase):
    def test_generated_unicode_files_are_utf8(self) -> None:
        generator = load_generator()
        with tempfile.TemporaryDirectory() as temporary:
            generator.PACK = Path(temporary) / "agent-workbench-pack"
            with contextlib.redirect_stdout(io.StringIO()):
                generator.main()

            rubric = generator.PACK / "docs" / "reviewer-rubric.md"
            handoff = generator.PACK / "scripts" / "generate_handoff.py"
            expected_rubric = generator.REVIEWER_RUBRIC_MD
            expected_handoff = generator.GENERATE_HANDOFF_PY

            self.assertEqual(rubric.read_text(encoding="utf-8"), expected_rubric)
            self.assertEqual(handoff.read_text(encoding="utf-8"), expected_handoff)


if __name__ == "__main__":
    unittest.main()
