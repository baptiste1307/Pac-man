import pygame
from dataclasses import dataclass, field
from mazegenerator.mazegenerator import MazeGenerator
from enum import Enum
from typing import Tuple, Any


class Colors(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    WALL_BLUE = (25, 25, 166)
    ULTRAMARINE = (33, 33, 222)
    PEACH = (222, 161, 133)
    RED = (255, 4, 8)
    GREEN = (0, 255, 0)

    D_BLUE = (33, 48, 187)
    CYAN = (168, 255, 246)
    B_YELLOW = (253, 255, 166)


@dataclass
class Level:
    width: int
    height: int
    cell_size: int = field(default=0)
    maze: MazeGenerator = field(default=None)

    def __post_init__(self):
        self.cell_size = self._find_cell_size(self.width, self.height)
        self.maze = MazeGenerator(size=(self.height, self.width))

    def _find_cell_size(self, level_width: int, level_height: int) -> int:

        # get current display's height & width
        info = pygame.display.Info()

        # adapt cell_size to be 70% of current level height or width
        # (depending on which one is the greatest)
        return min(
            (info.current_w * 0.7) // level_width,
            (info.current_h * 0.7) // level_height,
        )


class Button:
    def __init__(self, rect_width: int,
                 rect_height: int,
                 rect_pos_x: int,
                 rect_pos_y: int,
                 text: str,
                 text_rect: Any,
                 stroke_thickness: int) -> None:
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.rect_pos_x = rect_pos_x
        self.rect_pos_y = rect_pos_y
        self.text = text
        self.text_rect = text_rect
        self.stroke_thickness = stroke_thickness

        # self.rect = (self.rect_pos_x, self.rect_pos_y,
        #              self.rect_width - self.stroke_thickness,
        #              self.rect_height - self.stroke_thickness)

