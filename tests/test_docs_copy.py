from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).parents[1] / "skills/docs-sync/scripts/copy_sources.py"
SPEC = importlib.util.spec_from_file_location("docs_copy", SCRIPT)
COPY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COPY)


class CopyTests(unittest.TestCase):
    def render(self, source):
        return COPY.render(
            source,
            title="Authoring conventions",
            repo="openhat-ai/toolang",
            sha="abc123",
            path="docs/authoring.md",
        )

    def test_relative_links_pin_the_source_and_keep_fragments(self):
        page = self.render(
            "# Upstream\n\nSee [input](design/call-input.md#terminology) and [home](../README.md).\n"
        )
        self.assertIn(
            "https://github.com/openhat-ai/toolang/blob/abc123/docs/design/call-input.md#terminology",
            page,
        )
        self.assertIn(
            "https://github.com/openhat-ai/toolang/blob/abc123/README.md", page
        )
        self.assertTrue(page.startswith("# Authoring conventions\n"))
        self.assertNotIn("# Upstream", page)

    def test_code_is_unchanged_and_mdx_escapes_only_prose(self):
        source = "# Upstream\n\n<T> {value} `a < b {x}`\n\n```too\nagic:\n  {{_}} [link](local.md)\n```\n"
        page = self.render(source)
        self.assertIn("&lt;T&gt; \\{value\\} `a < b {x}`", page)
        self.assertIn("```too\nagic:\n  {{_}} [link](local.md)\n```", page)

    def test_absolute_links_and_same_page_anchors_are_preserved(self):
        source = "# Upstream\n\n[web](https://example.test/x) [section](#part)\n"
        page = self.render(source)
        self.assertIn("[web](https://example.test/x) [section](#part)", page)
        self.assertEqual(page, self.render(source))


if __name__ == "__main__":
    unittest.main()
