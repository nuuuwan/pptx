import os
import unittest

from powerpoint import PPTXFile


class TestPPTXFile(unittest.TestCase):
    TEST_PPTX_PATH = os.path.abspath(
        os.path.join('tests', 'test_data', 'test.pptx')
    )

    def test_notes_list(self):
        pptx = PPTXFile(self.TEST_PPTX_PATH)
        self.assertEqual(
            pptx.notes_list,
            [
                '\n'.join(
                    [
                        'The note on the first line says: A.I. is very cool. '
                        + 'A.I. is the future. I love A.I ',
                        '',
                        'Second line of notes. ',
                        '',
                        'Third line of notes.',
                    ]
                )
            ],
        )

    def test_image_path_list(self):
        pptx = PPTXFile(self.TEST_PPTX_PATH)
        for image_path in pptx.image_path_list:
            self.assertTrue(os.path.exists(image_path))
