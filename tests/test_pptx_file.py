import os
import shutil
import unittest

from powerpoint import PPTXFile

TEST_PPTX_PATH = os.path.abspath(os.path.join('tests', 'test.pptx'))


class TestPPTXFile(unittest.TestCase):
    def setUp(self):
        shutil.rmtree(os.path.join('tests', 'test-files'), ignore_errors=True)

    # def tearDown(self):
    #     self.setUp()

    def test_general(self):
        pptx = PPTXFile(TEST_PPTX_PATH)
        self.assertEqual(
            pptx.notes_list,
            [
                [
                    'The note on the first line says: A.I. is very cool. A.I. is the future. I love A.I..',
                    '',
                    'Second line of notes. ',
                    '',
                    'Third line of notes.',
                ]
            ],
        )

    def test_image_path_list(self):
        pptx = PPTXFile(TEST_PPTX_PATH)
        for image_path in pptx.image_path_list:
            self.assertTrue(os.path.exists(image_path))

    def test_write_video(self):
        pptx = PPTXFile(TEST_PPTX_PATH)
        video_path = pptx.write_video()
        self.assertTrue(os.path.exists(video_path))
