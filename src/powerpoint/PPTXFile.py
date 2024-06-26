from pptx import Presentation
from utils_future import TTSFile


class PPTXFile:
    DELIM_NOTES = '\n'

    def __init__(self, file_path):
        self.file_path = file_path

    @property
    def presentation(self) -> Presentation:
        return Presentation(self.file_path)

    @property
    def notes_list(self) -> list[str]:
        notes_list = []
        for slide in self.presentation.slides:
            notes = slide.notes_slide.notes_text_frame.text.split(
                PPTXFile.DELIM_NOTES
            )
            # filter out links
            notes = [note for note in notes if 'http' not in note]
            notes_list.append(notes)
        return notes_list

    def write_audio(self, audio_path: str):
        tts = TTSFile(audio_path)
        lines = [
            PPTXFile.DELIM_NOTES.join(notes) for notes in self.notes_list
        ]
        tts.write(lines)
