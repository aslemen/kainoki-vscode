import glob
from pathlib import Path
from trender import TRender
from pynt import task

@task()
def syntax():
    print("Generating the syntax highlighter ...")

    # 1. Identify paths to tag definitions
    files = {path.name: path for path in filter(
                                        lambda path: path.is_file(),
                                        map(
                                            Path,
                                            glob.iglob(
                                                "./source/tags/**",
                                                recursive = True
                                                )
                                            )
                                        )}

    # 2. Load files
    tags = dict()

    for fname, fpath in files.items():
        with fpath.open() as fstream:
            tags[fname] = [line.rstrip() for line in fstream]

    # 3. Generate the definition of "nodes": non_terminals + terminals
    if "nodes" in tags:
        raise Exception("It seems that you've already got the file ./source/tags/nodes, which is not supposed to exist!")

    tags["nodes"] = tags["terminals"] + tags["non_terminals"]

    # 4. Sort tags:
    for _, tag_contents in tags.items():
        tag_contents.sort(key = len, reverse = True)

    # 5. Concatenate them with "|"
    regexes = {tag_kind: "|".join(tag_contents) for tag_kind, tag_contents in tags.items()}

    # 6. Do templating
    result: str = None

    with open("./source/kai.syntax.template") as temp:
        template = TRender(temp.read())
        result = template.render(regexes)

    # 7. Write it into ./syntaxes/kai.tmLanguage.json (allowing overwriting)
    with open("./syntaxes/kai.tmLanguage.json", mode="w") as syn:
        syn.write(result)

    with open("./source/kail.syntax.template") as temp:
        template = TRender(temp.read())
        result = template.render(regexes)

    # 7. Write it into ./syntaxes/kai.tmLanguage.json (allowing overwriting)
    with open("./syntaxes/kail.tmLanguage.json", mode="w") as syn:
        syn.write(result)
    # ===END===
