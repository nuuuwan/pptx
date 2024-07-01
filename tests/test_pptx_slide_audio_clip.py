import os
import shutil
import tempfile
import unittest

from utils import Hash

from powerpoint import PPTXSlideAudioClip


class TestPPTXSlideAudioClip(unittest.TestCase):
    TEST_DIR_PATH = os.path.join(
        tempfile.gettempdir(),
        'TestPPTXSlideAudioClip',
    )
    TEST_TEXT = 'First line of notes'
    HASH = Hash.md5(TEST_TEXT)
    TEST_EXPECTED_AUDIO_PATH = os.path.join(
        TEST_DIR_PATH,
        'audio-clips',
        f'{HASH}.mp3',
    )

    def setUp(self):
        if os.path.exists(self.TEST_DIR_PATH):
            shutil.rmtree(self.TEST_DIR_PATH)
        os.makedirs(self.TEST_DIR_PATH)

    def test_build(self):
        audio_clip = PPTXSlideAudioClip(
            self.TEST_DIR_PATH,
            self.TEST_TEXT,
            True,
            True,
        ).build()
        self.assertGreaterEqual(
            audio_clip.duration * 1_000,
            PPTXSlideAudioClip.START_DURATION_FOR_FIRST
            + PPTXSlideAudioClip.END_DURATION_FOR_LAST,
        )
        self.assertTrue(os.path.exists(self.TEST_EXPECTED_AUDIO_PATH))
