"""Tests for instance LTCE-05: they pin the observable behavior of run().

Only run() is imported. The parser handles only closing tags here (opening
tags and text are ignored by the base class), so each test sets the state
before the html. The refactoring may replace the conditional expression with
an if statement; what must not change is the table of contents and the state
left by each closing tag.
"""

import pytest

from LTCE_05 import run


def test_typical_headers_indent_the_table_of_contents():
    state = run("<h1></h1><h2></h2><h3></h3>")

    assert state["toc"] == [("Intro", "1.0"), ("    Intro", "2.0"), ("        Intro", "3.0")]
    assert state["tags"] == ""
    assert state["prevtag"] == (False, "h3")


def test_edge_hidden_headers_and_other_closing_tags():
    assert run("<h2></h2>", show=False)["toc"] == []
    state = run("<span></span><a></a><pre></pre><p></p>")
    assert (state["chartags"], state["hdrlink"], state["pre"], state["tags"]) == ("", False, False, "")
    assert state["prevtag"] == (False, "p")
    nested = run("<dd></dd>", level=2)
    assert (nested["level"], nested["tags"]) == (1, "l1")
    closed = run("<ul></ul>", level=1)
    assert (closed["level"], closed["tags"]) == (0, "")


def test_invalid_header_closed_inside_an_indented_block():
    with pytest.raises(AssertionError):
        run("<h2></h2>", level=1)
