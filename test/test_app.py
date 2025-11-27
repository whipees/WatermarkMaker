import unittest
import sys
import os
import shutil
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import config, image_processing


class TestKonfigurace(unittest.TestCase):
    def test_paths_exist(self):
        self.assertIsInstance(config.INPUT_FOLDER, str)
        self.assertIsInstance(config.OUTPUT_FOLDER, str)

    def test_worker_count(self):
        self.assertGreater(config.NUM_WORKERS, 1)

    def setUp(self):

        self.test_dir = os.path.dirname(__file__)
        self.fake_input = os.path.join(self.test_dir, "temp_input")
        self.fake_output = os.path.join(self.test_dir, "temp_output")
        self.fake_error = os.path.join(self.test_dir, "temp_error")

        os.makedirs(self.fake_input, exist_ok=True)
        os.makedirs(self.fake_output, exist_ok=True)
        os.makedirs(self.fake_error, exist_ok=True)

        self.dummy_watermark = os.path.join(self.test_dir, "temp_watermark.png")
        img = Image.new('RGBA', (50, 50), color='red')
        img.save(self.dummy_watermark)

    def tearDown(self):
        shutil.rmtree(self.fake_input, ignore_errors=True)
        shutil.rmtree(self.fake_output, ignore_errors=True)
        shutil.rmtree(self.fake_error, ignore_errors=True)
        if os.path.exists(self.dummy_watermark):
            os.remove(self.dummy_watermark)

    def test_corrupt_file_handling(self):

        bad_filename = "fake_image.jpg"
        bad_filepath = os.path.join(self.fake_input, bad_filename)

        with open(bad_filepath, "w") as f:
            f.write("Tohle není obrázek, tohle je text převlečený za obrázek.")


        try:
            image_processing.apply_watermark(
                bad_filepath,
                self.dummy_watermark,
                self.fake_output,
                bad_filename
            )
            self.fail("Poškozený obrázek měl vyvolat chybu, ale nevyvolal!")

        except ValueError:

            shutil.move(bad_filepath, os.path.join(self.fake_error, bad_filename))

        self.assertFalse(os.path.exists(bad_filepath))

        error_path = os.path.join(self.fake_error, bad_filename)
        self.assertTrue(os.path.exists(error_path))


if __name__ == '__main__':
    unittest.main()