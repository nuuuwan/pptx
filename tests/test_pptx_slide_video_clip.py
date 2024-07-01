import os
import shutil
import tempfile
import unittest

from utils import Hash

from powerpoint import PPTXSlideVideoClip


class TestPPTXSlideVideoClip(unittest.TestCase):
    TEST_IMAGE_PATH = os.path.join('tests', 'test_data', 'test_image.png')
    TEST_DIR_PATH = os.path.join(
        tempfile.gettempdir(),
        'TestPPTXSlideVideoClip',
    )
    TEST_TEXT = 'First line of notes'
    HASH = Hash.md5(TEST_TEXT)
    TEST_EXPECTED_VIDEO_PATH = os.path.join(
        TEST_DIR_PATH,
        'video-clips',
        f'{HASH}.mp4',
    )

    def setUp(self):
        if os.path.exists(self.TEST_DIR_PATH):
            shutil.rmtree(self.TEST_DIR_PATH)
        os.makedirs(self.TEST_DIR_PATH)

    def test_build(self):
        PPTXSlideVideoClip(
            self.TEST_DIR_PATH,
            self.TEST_IMAGE_PATH,
            self.TEST_TEXT,
            True,
            True,
        ).build()
        self.assertTrue(os.path.exists(self.TEST_EXPECTED_VIDEO_PATH))
