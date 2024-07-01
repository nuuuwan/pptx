import os

from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip
from utils import Hash, Log

from powerpoint.PPTXSlideAudioClip import PPTXSlideAudioClip

log = Log('PPTXSlideVideoClip')


class PPTXSlideVideoClip:
    def __init__(
        self,
        dir_path: str,
        image_path: str,
        text: str,
        is_first: bool,
        is_last: bool,
    ):
        self.dir_path = dir_path
        self.image_path = image_path
        self.text = text
        self.is_first = is_first
        self.is_last = is_last

    @property
    def video_path(self) -> str:
        h = Hash.md5(self.text)
        video_path = os.path.join(self.dir_path, 'video-clips')
        os.makedirs(video_path, exist_ok=True)
        return os.path.join(video_path, f'{h}.mp4')

    @staticmethod
    def build_video(
        video_path: str, image_path: str, audio_clip: AudioFileClip
    ):
        clip = (
            ImageClip(image_path)
            .set_duration(audio_clip.duration)
            .set_audio(audio_clip)
        )
        clip.write_videofile(video_path, fps=24, verbose=False)
        log.info(f'Wrote {video_path}')

        return VideoFileClip(video_path)

    def build_nocache(self):
        audio_clip = PPTXSlideAudioClip(
            self.dir_path, self.text, self.is_first, self.is_last
        ).build()

        video_clip = PPTXSlideVideoClip.build_video(
            self.video_path, self.image_path, audio_clip
        )
        return video_clip

    def build(self):
        if os.path.exists(self.video_path):
            log.debug(f'Exists {self.video_path}')
            return VideoFileClip(self.video_path)
        return self.build_nocache()
