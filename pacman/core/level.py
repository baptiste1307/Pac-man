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

        r_width, r_height = (
            self.game.black_rectangle_width,
            self.game.black_rectangle_height,
        )

        return int(
            min(
                (r_height * 0.9) // level_height,
                (r_width * 0.9) // level_width,
            )
        )
