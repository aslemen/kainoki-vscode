#! /bin/python3

import glob
from pathlib import Path
from trender import TRender

files = map(
        lambda path: (path.name, path),
        filter(
            lambda path: path.is_file(),
            map(
                Path,
                glob.iglob(
                    "./tags/**",
                    recursive = True
                    )
                )
            )
        )

regexes = {}
for fname, fpath in files:
    with fpath.open() as fstream:
        regexes[fname] = "|".join(
                sorted(
                    map(
                        lambda x: x.rstrip(),
                        fstream
                        ),
                    reverse = True
                    )
                )

with open("./syntax.template") as temp:
    template = TRender(temp.read())
    print(template.render(regexes))
