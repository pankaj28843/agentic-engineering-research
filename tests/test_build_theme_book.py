from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from argparse import Namespace
from pathlib import Path, PurePosixPath
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_theme_book.py"
SPEC = importlib.util.spec_from_file_location("build_theme_book", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

PDF_INTEGRATION_TOOLS = ("pandoc", "xelatex", "pdftotext", "fc-match", "fc-query")
PDF_INTEGRATION_AVAILABLE = all(shutil.which(tool) for tool in PDF_INTEGRATION_TOOLS)


def write_theme(root: Path, name: str) -> Path:
    theme = root / name
    guide = theme / "guide"
    fixture = guide / "fixtures" / "demo"
    fixture.mkdir(parents=True)
    (theme / "README.md").write_text(f"# {name} title\n", encoding="utf-8")
    (theme / "source-index.md").write_text(
        "# Source index\n\n[Guide](guide/00-README.md)\n",
        encoding="utf-8",
    )
    (guide / "00-README.md").write_text(
        "# Guide\n\n[Chapter one](01-one.md)\n\n"
        "[Fixture](fixtures/demo/example.json)\n\n"
        "[Sources](../source-index.md)\n\n"
        "[Unpublished](../sources.json)\n",
        encoding="utf-8",
    )
    (guide / "01-one.md").write_text(
        "# Chapter one\n\nBack to the [guide](00-README.md).\n",
        encoding="utf-8",
    )
    (fixture / "example.json").write_text('{"fixture": true}\n', encoding="utf-8")
    return theme


def args(**overrides: object) -> Namespace:
    values = {
        "theme_dirs": [],
        "all_themes": False,
        "combined": False,
        "output_root": ROOT / "tmp" / "book-tests-output",
        "formats": "markdown",
        "title": None,
        "combined_title": "Combined",
        "combined_slug": "combined",
        "author": "Test Author",
        "copy_mobi_to": None,
    }
    values.update(overrides)
    return Namespace(**values)


class BuildThemeBookTests(unittest.TestCase):
    def setUp(self) -> None:
        (ROOT / "tmp").mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / "tmp")
        self.temp_root = Path(self.temp.name)
        self.research = self.temp_root / "research"
        self.research.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_explicit_theme_preserves_links_and_appends_evidence(self) -> None:
        theme = write_theme(self.research, "01-test-theme")
        spec = MODULE.BookSpec(
            slug=theme.name,
            title="Test book",
            themes=(theme,),
            output_dir=self.temp_root / "out",
        )

        markdown_path, _ = MODULE.build_markdown(spec, "Test Author")
        text = markdown_path.read_text(encoding="utf-8")

        self.assertIn(
            "[Chapter one](#pub-01-test-theme-guide-01-one)",
            text,
        )
        self.assertIn(
            "[Fixture](#pub-01-test-theme-guide-fixtures-demo-example)",
            text,
        )
        self.assertIn(
            "[Sources](#pub-01-test-theme-source-index)",
            text,
        )
        self.assertIn("# Evidence appendix — 01-test-theme title", text)
        self.assertIn('## `guide/fixtures/demo/example.json`', text)
        self.assertIn('{"fixture": true}', text)
        self.assertIn("Unpublished", text)
        self.assertNotIn("../sources.json", text)

    def test_all_combined_and_all_plus_combined_select_expected_specs(self) -> None:
        first = write_theme(self.research, "01-first")
        second = write_theme(self.research, "02-second")
        with patch.object(MODULE, "RESEARCH_ROOT", self.research):
            all_specs = MODULE.build_specs(args(all_themes=True))
            combined_specs = MODULE.build_specs(args(combined=True))
            both_specs = MODULE.build_specs(args(all_themes=True, combined=True))

        self.assertEqual([spec.themes for spec in all_specs], [(first,), (second,)])
        self.assertEqual(len(combined_specs), 1)
        self.assertEqual(combined_specs[0].themes, (first, second))
        self.assertEqual(len(both_specs), 3)
        self.assertTrue(both_specs[-1].combined)

    @unittest.skipUnless(shutil.which("pandoc"), "pandoc is required for EPUB integrity")
    def test_epub_internal_hrefs_resolve(self) -> None:
        theme = write_theme(self.research, "01-test-theme")
        output = self.temp_root / "epub"
        spec = MODULE.BookSpec(
            slug=theme.name,
            title="Test book",
            themes=(theme,),
            output_dir=output,
        )
        markdown_path, _ = MODULE.build_markdown(spec, "Test Author")
        epub_path = output / "test.epub"
        MODULE.run_pandoc(
            markdown_path,
            epub_path,
            title="Test book",
            author="Test Author",
        )

        with zipfile.ZipFile(epub_path) as archive:
            names = set(archive.namelist())
            documents = {
                name: archive.read(name).decode("utf-8")
                for name in names
                if name.endswith((".xhtml", ".html", ".htm"))
            }

        ids_by_document = {
            name: set(re.findall(r'\bid=["\']([^"\']+)["\']', text))
            for name, text in documents.items()
        }
        unresolved: list[str] = []
        for source_name, text in documents.items():
            for href in re.findall(r'\bhref=["\']([^"\']+)["\']', text):
                if not href or href.startswith(("http:", "https:", "mailto:")):
                    continue
                target_path, marker, fragment = href.partition("#")
                if not marker:
                    continue
                if target_path:
                    source_parent = PurePosixPath(source_name).parent
                    target_name = str(source_parent / PurePosixPath(target_path))
                else:
                    target_name = source_name
                if target_name not in names or fragment not in ids_by_document.get(
                    target_name, set()
                ):
                    unresolved.append(f"{source_name} -> {href}")

        self.assertEqual(unresolved, [])

    @unittest.skipUnless(shutil.which("pandoc"), "pandoc is required for EPUB styling")
    def test_epub_canvas_is_plain_and_reader_owned(self) -> None:
        markdown = self.temp_root / "plain.md"
        markdown.write_text(
            "# Plain book\n\n"
            "The device should own the reading canvas, colors, font, and margins.\n",
            encoding="utf-8",
        )
        epub_path = self.temp_root / "plain.epub"

        MODULE.run_pandoc(
            markdown,
            epub_path,
            title="Plain book",
            author="Test Author",
        )

        with zipfile.ZipFile(epub_path) as archive:
            stylesheet = "\n".join(
                archive.read(name).decode("utf-8")
                for name in archive.namelist()
                if name.endswith(".css")
            )

        self.assertRegex(
            stylesheet,
            r"(?s)@page\s*\{[^}]*margin:\s*0(?:[;\s}]|$)",
        )
        self.assertRegex(
            stylesheet,
            r"(?s)html,\s*body\s*\{[^}]*margin:\s*0(?:[;\s}]|$)"
            r"[^}]*padding:\s*0(?:[;\s}]|$)"
            r"[^}]*background:\s*transparent(?:[;\s}]|$)",
        )
        self.assertNotIn("background-color: #fdfdfd", stylesheet)
        self.assertNotIn("font-family: Georgia", stylesheet)
        self.assertNotIn("color: #1a1a1a", stylesheet)

    def test_pdf_requires_unicode_engine(self) -> None:
        markdown = self.temp_root / "input.md"
        markdown.write_text("# Unicode\n\n↘ ≈ ─\n", encoding="utf-8")
        with (
            patch.object(
                MODULE.shutil,
                "which",
                side_effect=lambda name: None if name == "xelatex" else f"/usr/bin/{name}",
            ),
            self.assertRaisesRegex(SystemExit, "xelatex not found.*Unicode-capable"),
        ):
            MODULE.run_pandoc(
                markdown,
                self.temp_root / "output.pdf",
                title="Unicode",
                author="Test Author",
            )

    def test_pdf_requires_pdftotext_validation(self) -> None:
        markdown = self.temp_root / "input.md"
        markdown.write_text("# Unicode\n\n↘ ≈ ─\n", encoding="utf-8")
        with (
            patch.object(
                MODULE.shutil,
                "which",
                side_effect=lambda name: None if name == "pdftotext" else f"/usr/bin/{name}",
            ),
            self.assertRaisesRegex(SystemExit, "pdftotext not found.*Poppler"),
        ):
            MODULE.run_pandoc(
                markdown,
                self.temp_root / "output.pdf",
                title="Unicode",
                author="Test Author",
            )

    def test_pdf_font_must_cover_publication_corpus(self) -> None:
        font = self.temp_root / "TestFont.ttf"
        font.write_bytes(b"test font placeholder")
        matched = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=f"Test Font\t{font}\n",
            stderr="",
        )
        ascii_only = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="20-7e\n",
            stderr="",
        )
        with (
            patch.object(MODULE, "run_captured", side_effect=[matched, ascii_only]),
            self.assertRaisesRegex(
                SystemExit,
                r"does not cover the publication corpus.*U\+2198",
            ),
        ):
            MODULE.require_font_coverage(
                "Test Font",
                "↘ ≈ ─",
                fc_match="/usr/bin/fc-match",
                fc_query="/usr/bin/fc-query",
            )

    def test_pdf_requires_exact_declared_font_family(self) -> None:
        fallback = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="Fallback Sans\t/usr/share/fonts/fallback.ttf\n",
            stderr="",
        )
        with (
            patch.object(MODULE, "run_captured", return_value=fallback),
            self.assertRaisesRegex(
                SystemExit,
                "required PDF font 'Required Sans' is unavailable",
            ),
        ):
            MODULE.require_font_coverage(
                "Required Sans",
                "↘ ≈ ─",
                fc_match="/usr/bin/fc-match",
                fc_query="/usr/bin/fc-query",
            )

    def test_pdf_missing_character_warning_is_fatal(self) -> None:
        markdown = self.temp_root / "input.md"
        markdown.write_text("# Unicode\n\n↘ ≈ ─\n", encoding="utf-8")
        output = self.temp_root / "output.pdf"
        output.write_bytes(b"incomplete")
        warning = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="",
            stderr="Missing character: There is no ↘ in font TestFont!",
        )
        with (
            patch.object(MODULE.shutil, "which", return_value="/usr/bin/pandoc"),
            patch.object(
                MODULE,
                "require_pdf_toolchain",
                return_value=("/usr/bin/xelatex", "/usr/bin/pdftotext"),
            ),
            patch.object(MODULE, "run_captured", return_value=warning),
            self.assertRaisesRegex(SystemExit, "missing-character.*missing-glyph"),
        ):
            MODULE.run_pandoc(
                markdown,
                output,
                title="Unicode",
                author="Test Author",
            )
        self.assertFalse(output.exists())

    @unittest.skipUnless(
        PDF_INTEGRATION_AVAILABLE,
        "Pandoc, XeLaTeX, Poppler, and fontconfig are required for PDF integration",
    )
    def test_pdf_round_trips_required_glyphs_in_body_and_code(self) -> None:
        markdown = self.temp_root / "unicode.md"
        markdown.write_text(
            "# Unicode publication\n\n"
            "Body glyphs: ↘ ≈ ─\n\n"
            "```text\n"
            "Code glyphs: ↘ ≈ ─\n"
            "```\n",
            encoding="utf-8",
        )
        output = self.temp_root / "unicode.pdf"

        MODULE.run_pandoc(
            markdown,
            output,
            title="Unicode publication",
            author="Test Author",
        )
        extracted = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", str(output), "-"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout

        for glyph in MODULE.PDF_REQUIRED_GLYPHS:
            self.assertGreaterEqual(extracted.count(glyph), 2)

    @unittest.skipUnless(
        PDF_INTEGRATION_AVAILABLE,
        "Pandoc, XeLaTeX, Poppler, and fontconfig are required for PDF integration",
    )
    def test_theme_09_complete_pdf_preserves_required_glyphs(self) -> None:
        theme = ROOT / "research" / "09-production-llm-systems-engineering"
        self.assertTrue(theme.is_dir())
        spec = MODULE.BookSpec(
            slug=theme.name,
            title=MODULE.theme_title(theme),
            themes=(theme,),
            output_dir=self.temp_root / "theme-09-pdf",
        )

        result = MODULE.build_book(spec, {"pdf"}, "Agentic Engineering Research")
        pdf = result.spec.output_dir / f"{theme.name}.pdf"
        extracted = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout

        for glyph in MODULE.PDF_REQUIRED_GLYPHS:
            self.assertIn(glyph, extracted)


if __name__ == "__main__":
    unittest.main()
