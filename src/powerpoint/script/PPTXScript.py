from dataclasses import dataclass

from utils import Log

from powerpoint.script.PPTXScriptSlide import PPTXScriptSlide
from pptx import Presentation
from pptx.util import Inches

log = Log('PPTXScript')


@dataclass
class PPTXScript:
    slides: list[PPTXScriptSlide]

    def write(self, pptx_path: str):
        prs = Presentation()

        for slide in self.slides:
            slide_layout = prs.slide_layouts[6]  # blank slide
            prs_slide = prs.slides.add_slide(slide_layout)

            if slide.text:
                textbox = prs_slide.shapes.add_textbox(
                    Inches(1), Inches(1), Inches(8), Inches(1.5)
                )
                text_frame = textbox.text_frame
                text_frame.text = '\n\n'.join(slide.text)

            if slide.images:
                log.warning('🤡 Only single image supported (#ForNow)')
                prs_slide.shapes.add_picture(
                    slide.images[0],
                    Inches(0),
                    Inches(0),
                    width=prs.slide_width,
                    height=prs.slide_height,
                )

            if slide.notes:
                notes_slide = prs_slide.notes_slide
                notes_text_frame = notes_slide.notes_text_frame
                notes_text_frame.text = '\n\n'.join(slide.notes)

        prs.save(pptx_path)
        log.info(f'Wrote {pptx_path}')

    def from_simple_config(config_lines):
        slides = []
        for line in config_lines:
            image_path, notes = line
            slides.append(
                PPTXScriptSlide(
                    text='',
                    images=[image_path],
                    notes=[notes],
                )
            )
        return PPTXScript(slides)
