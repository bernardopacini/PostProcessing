from glob import glob
import shutil
import os
from sphinx_gallery.scrapers import figure_rst
import kaleido
kaleido.get_chrome_sync()


def png_scraper(block, block_vars, gallery_conf):
    # Find all PNG files in the directory of this example.
    path_current_example = os.path.dirname(block_vars["src_file"])
    pngs = sorted(glob(os.path.join(path_current_example, "*.png")))

    # Iterate through PNGs, copy them to the Sphinx-Gallery output directory
    image_names = list()
    image_path_iterator = block_vars["image_path_iterator"]
    seen = set()
    for png in pngs:
        if png not in seen:
            seen |= set(png)
            this_image_path = image_path_iterator.next()
            image_names.append(this_image_path)
            shutil.move(png, this_image_path)

    # Use the `figure_rst` helper function to generate reST for image files
    return figure_rst(image_names, gallery_conf["src_dir"])
