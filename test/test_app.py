import unittest
import sys
import os
import shutil
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import config, image_processing


class TestConfiguration(unittest.TestCase):
    """
    Unit tests for configuration settings and error handling in file processing
    """


    def setUp(self):
        """
        Set up for tests (temporary directories, watermark)
        """
        self.test_dir = os.path.dirname(__file__)
        self.fake_input = os.path.join(self.test_dir, "temp_input")
        self.fake_output = os.path.join(self.test_dir, "temp_output")
        self.fake_error = os.path.join(self.test_dir, "temp_error")

        os.makedirs(self.fake_input, exist_ok=True)
        os.makedirs(self.fake_output, exist_ok=True)
        os.makedirs(self.fake_error, exist_ok=True)

        self.fake_watermark = os.path.join(self.test_dir, "temp_watermark.png")
        img = Image.new('RGBA', (50, 50), color='red')
        img.save(self.fake_watermark)

    def tearDown(self):
        """
        clean up after testing
        """
        shutil.rmtree(self.fake_input, ignore_errors=True)
        shutil.rmtree(self.fake_output, ignore_errors=True)
        shutil.rmtree(self.fake_error, ignore_errors=True)
        if os.path.exists(self.fake_watermark):
            os.remove(self.fake_watermark)


    def test_paths_exist(self):
        """
        tests, if paths are strings
        """
        self.assertIsInstance(config.INPUT_FOLDER, str)
        self.assertIsInstance(config.OUTPUT_FOLDER, str)

    def test_worker_count(self):
        """
        testing parralel worker count
        """
        self.assertGreater(config.NUM_WORKERS, 1)

    def test_valid_processing(self):
        """
        HAPPY PATH testing the good way scenario
        """
        filename = "valid_test.jpg"
        filepath = os.path.join(self.fake_input, filename)
        img = Image.new('RGB', (200, 200), color='blue')
        img.save(filepath)

        try:
            result = image_processing.apply_watermark(
                filepath,
                self.fake_watermark,
                self.fake_output,
                filename
            )
            self.assertTrue(result)
        except Exception as e:
            self.fail(f"Zpracování validního obrázku selhalo s chybou: {e}")

        expected_output = os.path.join(self.fake_output, f"watermarked_{filename}")

        self.assertTrue(os.path.exists(expected_output), "Výstupní soubor nebyl vytvořen!")

    def test_corrupt_file_handling(self):
        """
        Testing corrupt file handling, string instead of img
        """
        bad_filename = "fake_image.jpg"
        bad_filepath = os.path.join(self.fake_input, bad_filename)

        with open(bad_filepath, "w") as f:
            f.write("Toto není obrázek.")

        try:
            image_processing.apply_watermark(
                bad_filepath,
                self.fake_watermark,
                self.fake_output,
                bad_filename
            )
            self.fail("Měla nastat chyba ValueError!")
        except ValueError:
            shutil.move(bad_filepath, os.path.join(self.fake_error, bad_filename))

        self.assertTrue(os.path.exists(os.path.join(self.fake_error, bad_filename)))


if __name__ == '__main__':
    unittest.main()