import os
import unittest

from powerpoint import PPTXScript, PPTXScriptSlide


class TestPPTXScript(unittest.TestCase):
    def test_write(self):
        script = PPTXScript(
            [
                PPTXScriptSlide(
                    text=['Title'],
                    images=[
                        os.path.join(
                            'tests', 'test_data', 'test-image-sl.jpg'
                        )
                    ],
                    notes=[
                        'The title says Title.',
                    ],
                )
            ]
        )
        script.write(os.path.join('tests', 'test_data', 'test-script.pptx'))

    def test_simple_config(self):
        PPTXScript.from_simple_config(
            [
                [
                    os.path.join('tests', 'test_data', 'test-image-sl.jpg'),
                    'The title says Title',
                ]
            ]
        ).write(os.path.join('tests', 'test_data', 'test-script-simple.pptx'))

    def test_md(self):
        PPTXScript.from_md(
            os.path.join('tests', 'test_data', 'test-script.md')
        ).write(os.path.join('tests', 'test_data', 'test-script-md.pptx'))
