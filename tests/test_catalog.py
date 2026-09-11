import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pixl import catalog


class CatalogTests(unittest.TestCase):
    def test_duplicate_sources_and_stable_exact_section_ranges(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            data = "# First\nalpha\n## Second\nbeta\n"
            (root / "one.md").write_text(data)
            (root / "two.md").write_text(data)
            result = catalog.build(root)
            self.assertEqual(len(result["documents"]), 2)
            self.assertEqual(len(result["duplicates"]), 1)
            sections = result["documents"][0]["sections"]
            self.assertEqual([(s["start"], s["end"]) for s in sections], [(1, 2), (3, 4)])
            first_id = sections[0]["id"]
            (root / "two.md").write_text("# Other\nchanged\n")
            changed = catalog.build(root)
            self.assertEqual(changed["documents"][0]["sections"][0]["id"], first_id)
            self.assertEqual(changed["duplicates"], [])

    def test_heading_like_code_does_not_create_fake_section(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "source.md").write_text("# Art\n```css\n# canvas {\n}\n```\n## End\n")
            sections = catalog.build(root)["documents"][0]["sections"]
            self.assertEqual([s["title"] for s in sections], ["Art", "End"])
