import os
import re
from docutils import nodes
from docutils.parsers.rst import Directive


def search_font_family():
    directory = os.path.dirname(os.path.abspath(__file__)) + "/../../../postprocessing/matplotlib/styles"
    pattern = re.compile(r"font\.sans-serif:\s*(.*)")

    fonts = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mplstyle"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                    matches = pattern.findall(content)
                    for match in matches:
                        if match not in fonts:
                            fonts.append(match)

    return fonts


class font_list(Directive):
    def run(self):
        items = search_font_family()
        bullet_list = nodes.bullet_list()
        for item in items:
            list_item = nodes.list_item("", nodes.paragraph(text=item))
            bullet_list += list_item

        return [bullet_list]


def setup(app):
    app.add_directive("generate_matplotlib_font_list", font_list)
