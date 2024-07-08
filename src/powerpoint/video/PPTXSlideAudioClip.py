import os

from gtts import gTTS
from moviepy.editor import AudioFileClip
from pydub import AudioSegment
from utils import Hash, Log

log = Log('PPTXSlideAudioClip')


class PPTXSlideAudioClip:
    PLAYBACK_SPEED = 1.2
    START_DURATION_FOR_FIRST = 2_000
    START_DURATION_FOR_NOT_FIRST = 1000
    END_DURATION_FOR_LAST = 10_000
    END_DURATION_FOR_NOT_LAST = 1000

    def __init__(
        self, dir_path: str, text: str, is_first: bool, is_last: bool
    ):
        self.dir_path = dir_path
        self.text = text
        self.is_first = is_first
        self.is_last = is_last

    @property
    def cleaned_text(self) -> str:
        x = self.text
        for before, after in [('Rs.', 'Rupees'), ('Matale', 'Marthalay')]:
            x = x.replace(before, after)
        return x

    @property
    def audio_path(self) -> str:
        h = Hash.md5(self.text)
        audio_path = os.path.join(self.dir_path, 'audio-clips')
        os.makedirs(audio_path, exist_ok=True)
        return os.path.join(audio_path, f'{h}.mp3')

    @property
    def start_duration(self) -> int:
        if self.is_first:
            return self.START_DURATION_FOR_FIRST
        return self.START_DURATION_FOR_NOT_FIRST

    @property
    def end_duration(self) -> int:
        if self.is_last:
            return self.END_DURATION_FOR_LAST
        return self.END_DURATION_FOR_NOT_LAST

    def build_start_audio_segment(self):
        return AudioSegment.silent(duration=self.start_duration)

    def build_end_audio_segment(self):
        return AudioSegment.silent(duration=self.end_duration)

    def build_body_audio_segment(self):
        tts = gTTS(self.cleaned_text, lang='en', slow=False)
        tts.save(self.audio_path)
        return AudioSegment.from_file(self.audio_path).speedup(
            playback_speed=self.PLAYBACK_SPEED
        )

    def build_nocache(self):
        audio = (
            self.build_start_audio_segment()
            + self.build_body_audio_segment()
            + self.build_end_audio_segment()
        )
        audio.export(self.audio_path, format='mp3')
        log.info(f'Wrote {self.audio_path}')
        audio_clip = AudioFileClip(self.audio_path)
        return audio_clip

    def build(self):
        if os.path.exists(self.audio_path):
            log.debug(f'Exists {self.audio_path}')
            return AudioFileClip(self.audio_path)
        return self.build_nocache()
