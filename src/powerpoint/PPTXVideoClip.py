import os
import shutil

from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    afx,
    concatenate_videoclips,
)
from utils import Log

from powerpoint.PPTXFile import PPTXFile
from powerpoint.PPTXSlideVideoClip import PPTXSlideVideoClip

log = Log('PPTXVideoClip')


class PPTXVideoClip:
    def __init__(self, pptx_file: PPTXFile, audio_background_path: str):
        self.pptx_file = pptx_file
        self.audio_background_path = audio_background_path

    @staticmethod
    def add_background_music(combined_video_clip, audio_background_path):
        audio_clip = afx.audio_loop(
            AudioFileClip(audio_background_path).volumex(0.5),
            duration=combined_video_clip.duration,
        )

        combined_audio_clip = CompositeAudioClip(
            [combined_video_clip.audio, audio_clip]
        )
        combined_video_clip.audio = combined_audio_clip
        log.debug(f'Added background music ({audio_background_path})')
        return combined_video_clip

    def save(self, combined_video_clip):
        combined_video_path = os.path.join(
            self.pptx_file.dir_path, 'video.mp4'
        )
        combined_video_clip.write_videofile(
            combined_video_path,
            fps=24,
        )
        log.info(f'Wrote {combined_video_path}')

        copy_video_path = self.pptx_file.file_path.replace(
            '.pptx', '-video.mp4'
        )
        shutil.copy(combined_video_path, copy_video_path)
        log.info(f'Copied to {copy_video_path}')

    def build(self):
        slide_video_clips = []
        n_slides = len(self.pptx_file.notes_list)
        for i_slide, (notes, image_path) in enumerate(
            zip(self.pptx_file.notes_list, self.pptx_file.image_path_list),
            start=1,
        ):
            is_first = i_slide == 1
            is_last = i_slide == n_slides
            slide_video_clips.append(
                PPTXSlideVideoClip(
                    self.pptx_file.dir_path,
                    image_path,
                    notes,
                    is_first,
                    is_last,
                ).build()
            )

        combined_video_clip = concatenate_videoclips(
            slide_video_clips, method="compose"
        )
        combined_video_clip = PPTXVideoClip.add_background_music(
            combined_video_clip, self.audio_background_path
        )

        self.save(combined_video_clip)

        return combined_video_clip
