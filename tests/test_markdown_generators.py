"""Tests for markdown_generator html_escape functions and talks.html_escape variant.

The markdown_generator scripts (publications.py, pubsFromBib.py, talks.py) execute
module-level side effects on import (reading TSV/bib files). We test the html_escape
functions by extracting their logic directly rather than importing the modules.
"""

import pytest


# Replicate the html_escape table used by publications.py and pubsFromBib.py
HTML_ESCAPE_TABLE = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
}


def html_escape_publications(text):
    """Mirrors publications.py / pubsFromBib.py html_escape."""
    return "".join(HTML_ESCAPE_TABLE.get(c, c) for c in text)


def html_escape_talks(text):
    """Mirrors talks.py html_escape (handles non-string input)."""
    if type(text) is str:
        return "".join(HTML_ESCAPE_TABLE.get(c, c) for c in text)
    else:
        return "False"


# ---------------------------------------------------------------------------
# Publications / pubsFromBib html_escape
# ---------------------------------------------------------------------------

class TestPublicationsHtmlEscape:
    def test_no_special_chars(self):
        assert html_escape_publications("Hello World") == "Hello World"

    def test_ampersand(self):
        assert html_escape_publications("A & B") == "A &amp; B"

    def test_double_quote(self):
        assert html_escape_publications('Say "hi"') == "Say &quot;hi&quot;"

    def test_single_quote(self):
        assert html_escape_publications("it's") == "it&apos;s"

    def test_all_special(self):
        assert html_escape_publications("""&"'""") == "&amp;&quot;&apos;"

    def test_empty_string(self):
        assert html_escape_publications("") == ""

    def test_only_normal_chars(self):
        text = "abc123!@#$%^*()_+-=[]{}|;:,.<>/?"
        # Only &, ", ' should be escaped; others pass through
        result = html_escape_publications(text)
        assert "&amp;" not in result  # no & in input
        assert "&quot;" not in result  # no " in input
        assert "&apos;" not in result  # no ' in input
        assert result == text


# ---------------------------------------------------------------------------
# Talks html_escape (with non-string guard)
# ---------------------------------------------------------------------------

class TestTalksHtmlEscape:
    def test_string_input(self):
        assert html_escape_talks("Hello & World") == "Hello &amp; World"

    def test_non_string_returns_false(self):
        assert html_escape_talks(123) == "False"
        assert html_escape_talks(None) == "False"
        assert html_escape_talks(45.6) == "False"

    def test_bool_is_not_str(self):
        # In Python, bool is a subclass of int, but type(True) is bool, not str
        assert html_escape_talks(True) == "False"

    def test_empty_string(self):
        assert html_escape_talks("") == ""

    def test_special_chars(self):
        assert html_escape_talks("A & B's \"paper\"") == "A &amp; B&apos;s &quot;paper&quot;"
