import os
import unittest

from powerpoint import PPTXScript


class TestPPTXScript(unittest.TestCase):
    def test_build(self):
        script = PPTXScript(
            text='Title',
            image=os.path.join('test_data', 'test_image.png'),
            notes=[
                'The title says Title.',
            ],
        )
        script.write('test-script.pptx')
