import os
import unittest

from powerpoint import ImageHighlight


class TestImageHighLight(unittest.TestCase):
    def test_get_fingerprint(self):
        image_path = os.path.join(
            'tests', 'test_data', '1904.png'
        )
        fp = ImageHighlight.get_fp(image_path, 400)
        self.assertEqual(len(fp), 9)
        self.assertEqual(len(fp[0]), 9)
        self.assertAlmostEqual(fp[0][0], 255.0, places=1)
    
    def test_write(self):
        image_path = os.path.join(
            'tests', 'test_data', '1905.png'
        )
        guide_image_path = os.path.join(
            'tests', 'test_data', '1904.png'
        )
        output_image_path = os.path.join(
            'tests', 'test_data', 'test-highlight-output.png'
        )
        ImageHighlight(image_path, guide_image_path, 400).write(output_image_path)
