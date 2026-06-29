from dataclasses import dataclass, field
from mazegenerator.mazegenerator import MazeGenerator
from typing import Any


@dataclass
class Level:
    width: int
    height: int
    game: Any
    cell_size: int = field(default=0)
    maze: MazeGenerator = field(default=None)

    def __post_init__(self):
        self.cell_size = self._find_cell_size(self.width, self.height)
        self.maze = MazeGenerator(size=(self.height, self.width))

    def _find_cell_size(self, level_width: int, level_height: int) -> int:

        rectangle_width, rectangle_height = (
            self.game.black_rectangle_width,
            self.game.black_rectangle_height,
        )
        fill_ratio = self.game.play_area_fill_ratio

        return int(
            min(
                (rectangle_height * fill_ratio) // level_height,
                (rectangle_width * fill_ratio) // level_width,
            )
        )
