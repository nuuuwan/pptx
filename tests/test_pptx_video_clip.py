import os
import unittest

from powerpoint import PPTXFile, PPTXVideoClip


class TestPPTXVideoClip(unittest.TestCase):
    TEST_PPTX_PATH = os.path.abspath(
        os.path.join('tests', 'test_data', 'test.pptx')
    )
    TEST_AUDIO_BACKGROUND_PATH = os.path.abspath(
        os.path.join('media', 'thelounge.mp3')
    )
    TEST_EXPECTED_VIDEO_PATH = TEST_PPTX_PATH.replace('.pptx', '-video.mp4')

    def setUp(self):
        if os.path.exists(self.TEST_EXPECTED_VIDEO_PATH):
            os.remove(self.TEST_EXPECTED_VIDEO_PATH)

    def test_build(self):
        pptx = PPTXFile(self.TEST_PPTX_PATH)
        PPTXVideoClip(pptx, self.TEST_AUDIO_BACKGROUND_PATH).build()
        self.assertTrue(os.path.exists(self.TEST_EXPECTED_VIDEO_PATH))
