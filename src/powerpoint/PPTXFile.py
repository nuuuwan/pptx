import os
import re
import tempfile
from functools import cached_property

import win32com.client
from utils import Log

from pptx import Presentation as PPTXPresentation

log = Log('PPTXFile')


class PPTXFile:
    def __init__(self, file_path):
        self.file_path = file_path

    @cached_property
    def presentation(self) -> PPTXPresentation:
        return PPTXPresentation(self.file_path)

    @cached_property
    def dir_path(self):
        file_name_only = os.path.basename(self.file_path).split('.')[0]
        dir_path = os.path.join(
            tempfile.gettempdir(), f'pptx-{file_name_only}'
        )
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    @cached_property
    def image_path_list(self) -> list[str]:
        image_dir_path = os.path.join(self.dir_path, 'slide-images')
        os.makedirs(image_dir_path, exist_ok=True)

        app = win32com.client.Dispatch("Powerpoint.Application")
        presentation = app.Presentations.Open(self.file_path)

        image_path_list = []
        for i, slide in enumerate(presentation.Slides):
            image_path = os.path.join(image_dir_path, f'{i:03d}.png')
            slide.Export(image_path, "PNG")
            image_path_list.append(image_path)
            log.debug(f'Wrote {image_path}')

        app.Quit()
        return image_path_list

    @staticmethod
    def clean_content(x: str) -> str:
        x = x.replace('AI', 'A.I.')
        x = x.replace('...', ' ')
        x = x.replace('..', ' ')
        x = x.replace('…', ' ')
        x = re.sub(r' +', ' ', x)
        return x

    @cached_property
    def notes_list(self) -> list[str]:
        notes_list = []
        for slide in self.presentation.slides:
            notes = PPTXFile.clean_content(
                slide.notes_slide.notes_text_frame.text
            )
            notes_lines = notes.split('\n')
            # filter out links
            notes_lines = [note for note in notes_lines if 'http' not in note]
            notes = '\n'.join(notes_lines)
            notes_list.append(notes)
        return notes_list
