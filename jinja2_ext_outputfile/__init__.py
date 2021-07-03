# -*- coding: utf-8 -*-
"""
This module provides a Jinja2 directive to capture the output within its block
and write it to an output file.

.. code-block:: jinja2

    {% outputfile "xxx.out" %}
    ...lorem ipsum...
    {% endoutputfile %}


.. note:: Rationale

    It is sometimes much easier to generate all data that is normally split-up
    into multiple files into one template file  that contains the logic
    how these parts are split-up. Otherwise, you would need to provide a
    multi-stage code generator.
"""

from __future__ import absolute_import, print_function
import codecs
import os.path

from jinja2 import nodes
from jinja2.ext import Extension


# -----------------------------------------------------------------------------
# JINJA2 EXTENSION:
# -----------------------------------------------------------------------------
class OutputFileExtension(Extension):
    """Jinja2 extension that redirects the output in its block to a file.

    .. code-block:: jinja2

        {% outputfile "<filename>" -%}
        ...lorem ipsum...
        {%- endoutputfile %}
    """
    tags = set(["outputfile"])
    encoding = "UTF-8"
    verbose = True

    def parse(self, parser):
        """Used by the Jinja2 parser to delegate parsing of the directive/tag.

        :param parser:  Parser to use.
        :return: Jinja2 node(s) for the parser.
        """
        lineno = next(parser.stream).lineno
        filename = parser.parse_expression()
        encoding = nodes.Const(self.encoding)
        # MAYBE: parser.stream.expect('name:encoding')
        # MAYBE: name = parser.stream.expect('name')
        body = parser.parse_statements(["name:endoutputfile"], drop_needle=True)

        # -- RETURN: nodes.CallBlock/Call that is executed later-on.
        return nodes.CallBlock(
            self.call_method("_output_to_file", [filename, encoding]),
            [], [], body).set_lineno(lineno)

    def _output_to_file(self, filename, encoding, caller):
        """Stores the output of the template-block in an output file.

        Extension/Tag core functionality, called by the CodeGenerator
        (when the parsed nodes are processed).

        :param filename:  File name of the output file.
        :param encoding:  File encoding to use (UTF-8, ...)
        :param caller:    Macro that encapsulates the template block contents.
        :return: Empty string (because block-contents are redirected to file).
        """
        captured_text = caller()

        basedir = os.path.dirname(filename) or "."
        if not os.path.isdir(basedir):
            os.makedirs(basedir)

        self._report_outfile(filename)
        with codecs.open(filename, mode="w+", encoding=encoding) as output:
            output.write(captured_text)
            output.write("\n")
            # output.flush()
        return ""

    def _report_outfile(self, filename):
        if self.verbose:
            annotation = ""
            if os.path.isfile(filename):
                annotation = "(overwritten)"
            print("OUTPUTFILE: %s ... %s" % (filename, annotation))
