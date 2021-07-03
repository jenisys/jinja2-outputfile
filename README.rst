Outputfile Extension for the Jinja2 Template Engine
===============================================================================

This python package provides a `Jinja2`_ directive that supports to redirect
blocks of a rendered template to one or more file(s), like::

.. code-block:: python

    # -- FILE: example.py
    from jinja2 import Environment

    the_template = """
    {%- for name in this.names -%}
        {% outputfile "%s/example_%s.txt"|format(this.output_dir, name) -%}
        Hello {{name}}
        {%- endoutputfile %}
    {% endfor %}
    """

    env = Environment(extensions=["jinja2_ext_outputfile.OutputFileExtension"])
    code_generator = env.from_string(the_template)
    code_generator.render(this=dict(names=["Alice", "Bob"], output_dir="."))

    # -- POSTCONDITION: CREATED FILES (with contents)
    #   * file:./example_Alice.txt:  Hello Alice
    #   * file:./example_Bob.txt     Hello Bob

.. _Jinja2:: https://github.com/pallets/jinja/


Rationale
-------------------------------------------------------------------------------

The ``outputfile`` directive is usefull in a code generator use case
if many output files need to be generated from Jinja2 templates.
In this case, you can provide one template as control script to accomplish this task.


History
-------------------------------------------------------------------------------

* INITIALLY CREATED AS: simplegen.jinja2_ext.outputfile
* REFACTORING: Extracted into own standalone package to simplify reuse
  with Jinja2 template engine.
