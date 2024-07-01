import os
import sys

from utils import Log

from powerpoint import PPTXFile, PPTXVideoClip

log = Log('build_notes_audio')


def main(pptx_path):
    pptx = PPTXFile(pptx_path)
    PPTXVideoClip(pptx, os.path.join('media', 'thelounge.mp3')).build()


if __name__ == "__main__":
    pptx_path = sys.argv[1]
    log.debug(f'{pptx_path=}')
    main(pptx_path)
