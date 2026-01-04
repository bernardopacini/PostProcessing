import os
import sys
import subprocess
import unittest
from parameterized import parameterized
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim


# Directory paths
example_dir = os.path.join(os.path.dirname(__file__), "../../examples/plotly")
baseline_dir = os.path.join(os.path.dirname(__file__), "../../input_data/DATA-PostProcessing/plotly")
output_dir = os.getcwd()


def run_example_script(script_path, output_dir):
    """
    Runs the example script and returns the path to the generated image.

    Parameters
    ----------
    script_path : str
        Path to script to be run.
    output_dir : str
        Path to image output directory.

    Returns
    -------
    image
        Image output from the example script.
    """
    script_name = os.path.splitext(os.path.basename(script_path))[0]
    output_image = os.path.join(output_dir, "{}.png".format(script_name[script_name.find("_") + 1 :]))

    subprocess.run("{} {}".format(sys.executable, script_path), shell=True, check=True)

    return output_image


def images_are_similar(img_1, img_2, tolerance=1.0):
    """
    Compares two images and returns True if they are similar within the given tolerance.

    Parameters
    ----------
    img_1 : image
        Image 1 for comparison.
    img_2 : image
        Image 2 for comparison.
    tolerance : float
        Comparison tolerance for match between images.

    Returns
    -------
    bool
        Boolean flag of whether or not the images are the same, within tolerance.
    """
    # Convert images to RGB and NumPy arrays
    img_1_RGB = np.array(img_1.convert("RGB"))
    img_2_RGB = np.array(img_2.convert("RGB"))

    # Compare images
    similarity_index, _ = ssim(img_1_RGB, img_2_RGB, multichannel=True, channel_axis=-1, full=True)

    return similarity_index >= tolerance


def get_example_scripts(example_dir):
    """
    Returns a list of all example scripts in the examples directory.

    Parameters
    ----------
    example_dir : str
        String specifying example scripts directory.

    Returns
    -------
    list
        List of strings of all the examples scripts in the examples directory.
    """
    return [os.path.join(example_dir, file) for file in os.listdir(example_dir) if file.endswith(".py")]


class TestPlotlyExamples(unittest.TestCase):

    @parameterized.expand(get_example_scripts(example_dir))
    def test_example(self, script_path):
        """
        Tests each example script by comparing the generated image to the baseline.

        Parameters
        ----------
        script_path : str
            Path to script to run and test.
        """
        # Define baseline and generate test image
        script_name = os.path.splitext(os.path.basename(script_path))[0]
        baseline_image_path = os.path.join(baseline_dir, "{}.png".format(script_name[script_name.find("_") + 1 :]))
        output_image_path = run_example_script(script_path, output_dir)

        # Load images
        baseline_image = Image.open(baseline_image_path)
        output_image = Image.open(output_image_path)

        # Compare images
        try:
            self.assertTrue(
                images_are_similar(baseline_image, output_image, tolerance=0.99),
                "Images differ for {}!".format(script_name),
            )

        # Delete test image
        finally:
            if os.path.exists(output_image_path):
                os.remove(output_image_path)


if __name__ == "__main__":
    unittest.main()
