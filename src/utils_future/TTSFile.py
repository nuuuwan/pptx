import os
import tempfile
from functools import cache

from gtts import gTTS
from pydub import AudioSegment
from utils import Hash, Log

log = Log('TTSFile')


class TTSFile:
    TEMP_AUDIO_DIR = os.path.join(tempfile.gettempdir(), 'tts_audio')
    PLAYBACK_SPEED = 1.25

    def __init__(self, audio_path: str):
        self.audio_path = audio_path

    @staticmethod
    @cache
    def write_line_in_temp(line: str) -> str:
        HASH_SALT = 'v0914'
        h = Hash.md5(line + HASH_SALT)
        os.makedirs(TTSFile.TEMP_AUDIO_DIR, exist_ok=True)
        temp_audio_path = os.path.join(TTSFile.TEMP_AUDIO_DIR, f'{h}.mp3')
        if not os.path.exists(temp_audio_path):
            tts = gTTS(text=line, lang='en', slow=False)
            tts.save(temp_audio_path)
        return temp_audio_path

    @staticmethod
    @cache
    def delim_audio_segment() -> AudioSegment:
        DELIM_AUDIO_SEGMENT_PATH = os.path.join(
            'src', 'utils_future', 'tabla-click.mp3'
        )
        return AudioSegment.from_file(DELIM_AUDIO_SEGMENT_PATH)

    @staticmethod
    def combine_audio(temp_audio_paths: list[str], combined_audio_path):
        combined = AudioSegment.empty()
        for temp_audio_path in temp_audio_paths:
            audio = AudioSegment.from_mp3(temp_audio_path)
            audio = audio.speedup(playback_speed=TTSFile.PLAYBACK_SPEED)
            combined += audio
            combined += TTSFile.delim_audio_segment()

        combined.export(combined_audio_path, format='mp3')

    def write(self, lines: list[str]):
        temp_audio_paths = []
        n = len(lines)
        for i, line in enumerate(lines, start=1):
            temp_audio_path = self.write_line_in_temp(line)
            temp_audio_paths.append(temp_audio_path)
            log.debug(f'{i}/{n} -> {temp_audio_path}')
        self.combine_audio(temp_audio_paths, self.audio_path)
        log.info(f'Wrote {n} segments to {self.audio_path}')
