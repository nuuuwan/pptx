import os

from powerpoint import PPTXFile, PPTXScript, PPTXVideoClip

BASE_DIR = os.path.dirname(__file__)
AUDIO_BACKGROUND_PATH = os.path.join('media', 'thelounge.mp3')


def image(year):
    return os.path.join(BASE_DIR, 'images', f'{year}.png')


def main():
    pptx_path = os.path.join(BASE_DIR, 'slides.pptx')

    PPTXScript.from_md(os.path.join(BASE_DIR, 'script.md')).write(
        pptx_path
    )

    PPTXVideoClip(PPTXFile(pptx_path), AUDIO_BACKGROUND_PATH).build()


if __name__ == "__main__":
    main()
