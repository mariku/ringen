#------------------------------------------------------------------------------

import click
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

#------------------------------------------------------------------------------


@click.command()
@click.option('-i', '--input-filename', required=True,
              type=Path)
@click.option('-o', '--output-dir', required=True,
              type=Path)
def generate(input_filename, output_dir):
    buffers = read(input_filename)
    for b in buffers.values():
        _generate(b, output_dir)

#------------------------------------------------------------------------------


def read(filename):
    r = Reader()
    r.read(filename)
    return r.buffers

#------------------------------------------------------------------------------


def _generate(buffer, output_dir):
    env = Environment(
        loader=FileSystemLoader([str(Path(__file__).parent / 'templates')]),
    )
    ct = env.get_template("default_c.tmpl")
    ht = env.get_template("default_h.tmpl")
    ctt = env.get_template("default_test_c.tmpl")

    output_dir.mkdir(parents=True, exist_ok=True)

    _generate_file(buffer, ct, output_dir / (buffer.prefix + '.c'))
    _generate_file(buffer, ht, output_dir / (buffer.prefix + '.h'))
    _generate_file(buffer, ctt, output_dir / (buffer.prefix + '_test.c'))

#------------------------------------------------------------------------------


def _generate_file(buffer, template, output_filename):
    with output_filename.open('w') as f:
        f.write(template.render(buffer=buffer))

#------------------------------------------------------------------------------


class Buffer:

    def __init__(self, prefix, typename, itemtype,
                 size_define, h_before_code=None,
                 h_after_code=None, c_before_code=None,
                 c_after_code=None):
        self.prefix = prefix
        self.typename = typename
        self.itemtype = itemtype
        self.size_define = size_define
        self.h_before_code = h_before_code
        self.h_after_code = h_after_code
        self.c_before_code = c_before_code
        self.c_after_code = c_after_code

#------------------------------------------------------------------------------


class Reader:

    def __init__(self):
        self.buffers = {}

    def api(self):
        return {
            "buffer": self._create_buffer,
        }

    def read(self, filename):
        exec(filename.open().read(), self.api(), {})

    def _create_buffer(self, prefix, typename, itemtype,
                       size_define, **kwargs):
        self.buffers[prefix] = Buffer(prefix, typename, itemtype,
                                      size_define, **kwargs)


#------------------------------------------------------------------------------

if __name__ == "__main__":
    generate()

#------------------------------------------------------------------------------
