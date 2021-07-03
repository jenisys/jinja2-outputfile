from __future__ import absolute_import, print_function
from codecs import open
from jinja2 import Template, Environment
import pytest


# -----------------------------------------------------------------------------
# UTILITY FUNCTIONS
# -----------------------------------------------------------------------------
def textfile_contents(filename):
    with open(str(filename), encoding="UTF-8") as f:
        contents = f.read()
    return contents


def assert_textfile_has_contents(filename, expected_contents):
    assert filename.exists()
    assert filename.is_file()
    actual_contents = textfile_contents(filename).rstrip()
    assert actual_contents == expected_contents

def assert_directory_has_files(directory, expected_files):
    actual_files = [str(p.name) for p in sorted(directory.iterdir()) if p.is_file()]
    assert actual_files == expected_files


# -----------------------------------------------------------------------------
# TEST SUITE
# -----------------------------------------------------------------------------
#    {% outputfile "{output_dir}/example_{name}.txt".format(output_dir=output_dir, name=name) -%}
def test_outputfile_basics(tmp_path):
    the_template = """
{% outputfile "%s/example_%s.txt"|format(this.output_dir, this.name) -%}
Hello {{this.name}}
{%- endoutputfile %}
"""

    env = Environment(extensions=["jinja2_ext_outputfile.OutputFileExtension"])
    code_generator = env.from_string(the_template)
    text = code_generator.render(this=dict(name="Alice", output_dir=str(tmp_path)))
    print(text)

    assert_textfile_has_contents(tmp_path/"example_Alice.txt", "Hello Alice")


def test_outputfile_with_forloop(tmp_path):
    the_template = """
{%- for name in this.names -%}
    {% outputfile "%s/example_%s.txt"|format(this.output_dir, name) -%}
    Hello {{name}}
    {%- endoutputfile %}
{%- endfor %}
"""

    names = ["Alice", "Bob"]
    env = Environment(extensions=["jinja2_ext_outputfile.OutputFileExtension"])
    code_generator = env.from_string(the_template)
    text = code_generator.render(this=dict(names=names, output_dir=str(tmp_path)))
    print(text)

    assert_directory_has_files(tmp_path, ["example_Alice.txt", "example_Bob.txt"])
    assert_textfile_has_contents(tmp_path/"example_Alice.txt", "Hello Alice")
    assert_textfile_has_contents(tmp_path/"example_Bob.txt", "Hello Bob")

def test_outputfile_creates_nonexisting_directory(tmp_path):
    the_template = """
{% outputfile "%s/subdir/example_%s.txt"|format(this.output_dir, this.name) -%}
Hello {{this.name}}
{%- endoutputfile %}
"""

    # -- PRECONDITION:
    subdir = tmp_path/"subdir"
    assert not subdir.exists()
    assert not subdir.is_dir()

    env = Environment(extensions=["jinja2_ext_outputfile.OutputFileExtension"])
    code_generator = env.from_string(the_template)
    text = code_generator.render(this=dict(name="Charly", output_dir=str(tmp_path)))
    print(text)

    assert_textfile_has_contents(tmp_path/"subdir/example_Charly.txt", "Hello Charly")
    assert subdir.exists()
    assert subdir.is_dir()
