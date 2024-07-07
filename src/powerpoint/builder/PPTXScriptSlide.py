from dataclasses import dataclass


@dataclass
class PPTXScriptSlide:
    text: list[str]
    images: list[str]
    notes: list[str]
