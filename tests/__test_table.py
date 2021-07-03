# -*- coding: utf-8 -*-
"""
Test module for unit-tests of the simplegen.jinja2_ext.table module.

REQUIRE: pytest
"""

from simplegen.jinja2_ext import table
import pytest
import textwrap


# ------------------------------------------------------------------------------
# TESTS:
# ------------------------------------------------------------------------------
class TestModule(object):

    def test_make_data_view(self):
        pass

    def test_render(self):
        table_data = [
            ("Alice", 1990),
            ("Bob",   2000),
        ]
        headers = ["Name", "Birthyear"]
        output = table.render(table_data, headers)
        expected = textwrap.dedent(
            """
            Name      Birthyear
            ------  -----------
            Alice          1990
            Bob            2000
            """).strip()
        assert output == expected

    def test_render__with_data_view(self):
        table_data = [
            dict(name="Alice", birthyear=1990),
            dict(name="Bob",   birthyear=2000),
        ]
        headers = ["Name", "Birthyear"]
        getters = [name.lower() for name in headers]
        data_view = table.make_dataview(getters)
        output = table.render(table_data, headers, data_view)
        expected = textwrap.dedent(
            """
            Name      Birthyear
            ------  -----------
            Alice          1990
            Bob            2000
            """).strip()
        assert output == expected

    def test_make_renderer(self):
        table_data = [
            ("Alice", 1990),
            ("Bob",   2000),
        ]
        headers = ["Name", "Birthyear"]

        render_table = table.make_renderer("plain")
        output = render_table(table_data, headers)
        expected = textwrap.dedent(
            """
            Name      Birthyear
            Alice          1990
            Bob            2000
            """).strip()
        assert output == expected

    def test_make_renderer__can_override_style(self):
        table_data = [
            ("Alice", 1990),
            ("Bob",   2000),
        ]
        headers = ["Name", "Birthyear"]

        render_table = table.make_renderer("plain")
        output = render_table(table_data, headers, style="simple")
        expected = textwrap.dedent(
            """
            Name      Birthyear
            ------  -----------
            Alice          1990
            Bob            2000
            """).strip()
        assert output == expected


    def test_collect_data(self):
        table_items = [
            dict(name="Alice", birthyear=1990),
            dict(name="Bob",   birthyear=2000),
        ]
        getters = ["name", "birthyear"]
        actual = table.collect_data(table_items, getters)
        expected = [
            ("Alice", 1990),
            ("Bob",   2000),
        ]
        assert actual, expected

    def test_collect_data__with_defaults(self):
        table_items = [
            dict(name="Alice", birthyear=1990, sex="female"),
            dict(name="Bob",   birthyear=None),
        ]
        getters = ["name", "birthyear", "sex"]
        defaults = {"sex": "unknown", "birthyear": 1900}
        actual = table.collect_data(table_items, getters, defaults)
        expected = [
            ("Alice", 1990, "female"),
            ("Bob",   None, "unknown"),  # USE: defaults["sex"] = "unknown"
        ]
        assert actual, expected


class TestTableStyle(object):
    """Tests all table styles to render a table."""

    style_expected_map = {
        "simple":   """
                    Name      Birthyear
                    ------  -----------
                    Alice          1990
                    Bob            2000
                    """,
        "plain":    """
                    Name      Birthyear
                    Alice          1990
                    Bob            2000
                    """,
        "grid":     """
                    +--------+-------------+
                    | Name   |   Birthyear |
                    +========+=============+
                    | Alice  |        1990 |
                    +--------+-------------+
                    | Bob    |        2000 |
                    +--------+-------------+
                    """,
        "fancy_grid": u"""
                    ╒════════╤═════════════╕
                    │ Name   │   Birthyear │
                    ╞════════╪═════════════╡
                    │ Alice  │        1990 │
                    ├────────┼─────────────┤
                    │ Bob    │        2000 │
                    ╘════════╧═════════════╛
                    """,
        "pipe":     """
                    | Name   |   Birthyear |
                    |:-------|------------:|
                    | Alice  |        1990 |
                    | Bob    |        2000 |
                    """,
        "orgtbl":   """
                    | Name   |   Birthyear |
                    |--------+-------------|
                    | Alice  |        1990 |
                    | Bob    |        2000 |
                    """,
        "rst":      """
                    ======  ===========
                    Name      Birthyear
                    ======  ===========
                    Alice          1990
                    Bob            2000
                    ======  ===========
                    """,
        "mediawiki": """
                    {| class="wikitable" style="text-align: left;"
                    |+ <!-- caption -->
                    |-
                    ! Name   !! align="right"|   Birthyear
                    |-
                    | Alice  || align="right"|        1990
                    |-
                    | Bob    || align="right"|        2000
                    |}
                    """,
         "html":    """
                    <table>
                    <thead>
                    <tr><th>Name  </th><th style="text-align: right;">  Birthyear</th></tr>
                    </thead>
                    <tbody>
                    <tr><td>Alice </td><td style="text-align: right;">       1990</td></tr>
                    <tr><td>Bob   </td><td style="text-align: right;">       2000</td></tr>
                    </tbody>
                    </table>
                    """,
        "latex":   r"""
                    \begin{tabular}{lr}
                    \hline
                     Name   &   Birthyear \\
                    \hline
                     Alice  &        1990 \\
                     Bob    &        2000 \\
                    \hline
                    \end{tabular}
                    """,
        "latex_booktabs": r"""
                    \begin{tabular}{lr}
                    \toprule
                     Name   &   Birthyear \\
                    \midrule
                     Alice  &        1990 \\
                     Bob    &        2000 \\
                    \bottomrule
                    \end{tabular}
                    """,
        "tsv":     """
                    Name  	  Birthyear
                    Alice 	       1990
                    Bob   	       2000
                    """,
        # -- TABULATE TABLE-FORMAT EXTENSIONS:
        "piped":    """
                    | Name   |   Birthyear |
                    | Alice  |        1990 |
                    | Bob    |        2000 |
                    """,
        # -- PRETTY-PRINTED CSV (for now, without quoting)
        "csv":      """
                    Name  ,  Birthyear
                    Alice ,       1990
                    Bob   ,       2000
                    """,
    }

    @pytest.mark.parametrize("style", [
        "simple", "plain", "grid", "fancy_grid", "pipe", "orgtbl", "rst",
        "mediawiki",
        "html",
        "latex", "latex_booktabs", "tsv",
        # -- TABULATE TABLE-FORMAT EXTENSIONS:
        "piped", "csv"
    ])
    def test_render__with_style(self, style):
        table_data = [
            ("Alice", 1990),
            ("Bob",   2000),
        ]
        headers = ["Name", "Birthyear"]
        output = table.render(table_data, headers, style=style)
        expected = textwrap.dedent(self.style_expected_map[style]).strip()
        assert output == expected


class TestLibrary(object):
    """Test that template library object has expected contents."""
    expected_filters = []
    expected_tests = []
    expected_globals = [
        ("table.render",        table.render),
        ("table.make_renderer", table.make_renderer),
        ("table.make_dataview", table.make_dataview),
        ("table.collect_data",  table.collect_data),
    ]
    expected_extensions = []

    def test_library_filters(self):
        assert table.library.filters == dict(self.expected_filters)

    def test_library_tests(self):
        assert table.library.tests == dict(self.expected_tests)

    def test_library_globals(self):
        assert table.library.globals == dict(self.expected_globals)

    def test_library_extensions(self):
        assert table.library.extensions == self.expected_extensions

