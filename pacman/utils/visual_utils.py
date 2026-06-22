import pygame
from dataclasses import dataclass, field
from mazegenerator.mazegenerator import MazeGenerator
from enum import Enum


class Colors(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    WALL_BLUE = (25, 25, 166)
    ULTRAMARINE = (33, 33, 222)
    PEACH = (222, 161, 133)
    RED = (253, 0, 0)
    GREEN = (0, 255, 0)


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
