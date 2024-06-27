import sys

from utils import Log

from powerpoint import PPTXFile

log = Log('build_notes_audio')


def main(pptx_path):
    pptx = PPTXFile(pptx_path)
    n_notes_list = []
    for notes in pptx.notes_list:
        content = ' '.join(notes)
        n_notes = len(content)
        n_notes_list.append(n_notes)

    avg_n_notes = sum(n_notes_list) / len(n_notes_list)
    for i, n_notes in enumerate(n_notes_list, start=1):
        p = n_notes / avg_n_notes
        emoji = ''
        if p > 2:
            emoji = '🔴'
        elif p > 1.5:
            emoji = '🟠'
        log.debug(
            f'slide-{i:02d}'.rjust(10)
            + f'{n_notes:,}'.rjust(10)
            + f'{p:.0%}'.rjust(10)
            + emoji
        )


if __name__ == "__main__":
    pptx_path = sys.argv[1]
    log.debug(f'{pptx_path=}')
    main(pptx_path)
