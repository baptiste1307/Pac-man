from typing import Any


class Button:
    def __init__(
        self,
        rect_width: int,
        rect_height: int,
        rect_pos_x: int,
        rect_pos_y: int,
        text: str,
        text_rect: Any,
        stroke_thickness: int,
    ) -> None:
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.rect_pos_x = rect_pos_x
        self.rect_pos_y = rect_pos_y
        self.text = text
        self.text_rect = text_rect
        self.stroke_thickness = stroke_thickness

        self.rect = (
            self.rect_pos_x,
            self.rect_pos_y,
            self.rect_width - self.stroke_thickness,
            self.rect_height - self.stroke_thickness,
        )
