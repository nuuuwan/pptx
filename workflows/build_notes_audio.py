import sys

from utils import Log

from powerpoint import PPTXFile

log = Log('build_notes_audio')


def main(pptx_path):
    pptx = PPTXFile(pptx_path)
    pptx.write_audio(pptx_path + '.mp3')


if __name__ == "__main__":
    pptx_path = sys.argv[1]
    log.debug(f'{pptx_path=}')
    main(pptx_path)
