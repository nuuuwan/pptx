import os
import unittest

from powerpoint import PPTXFile

TEST_PPTX_PATH = os.path.join('tests', 'test.pptx')
TEST_AUDIO_PATH = os.path.join('tests', 'test.mp3')


class TestPPTXFile(unittest.TestCase):
    def test_general(self):
        pptx = PPTXFile(TEST_PPTX_PATH)
        self.assertEqual(
            pptx.notes_list,
            [
                [
                    'Notes on first slides.',
                    '',
                    'Second line of notes. ',
                    '',
                    'Third line of notes.',
                ]
            ],
        )

    def test_write_audio(self):
        pptx = PPTXFile(TEST_PPTX_PATH)

        if os.path.exists(TEST_AUDIO_PATH):
            os.remove(TEST_AUDIO_PATH)
        pptx.write_audio(TEST_AUDIO_PATH)
        self.assertTrue(os.path.exists(TEST_AUDIO_PATH))
