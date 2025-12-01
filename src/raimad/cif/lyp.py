from dataclasses import Dataclass

@dataclass
class Properties:
    expanded: bool
    frame_color: str
    fill_color: str
    frame_brightness: int
    fill_brightness: int
    dither_pattern: str
    line_style: str
    valid: bool
    visible: bool
    transparent: bool
    width: int
    marked: bool
    xfill: bool
    animation: int
    name: str
    #klay_source: str


