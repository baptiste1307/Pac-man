from typing import Any
from dataclasses import dataclass

from .statistics import Statistics

from .level import Level


def get_levels(config: dict[str, Any]) -> list[Level]:
    levels: list[Level] = []

    for level in config["levels"]:
        new_level = Level(width=level["width"], height=level["height"])
        levels.append(new_level)

    return levels


@dataclass
class GameState:
    config: dict[str, Any]
    current_level: int = 0
    pacman_speed: int = 4
    direction: str = "right"
    current_frame: int = 0
    animation_timer: int = 0
    animation_delay: int = 60
    MAZE_OFFSET_X = 25
    MAZE_OFFSET_Y = 125
    level_timer: int = 0

    def __post_init__(self):
        self.levels = get_levels(self.config)
        self.reset_level()

    def update_target_position(self) -> None:
        self.target_x = (
            self.MAZE_OFFSET_X + self.pacman_grid_x * self.current_cell_size
        )

        self.target_y = (
            self.MAZE_OFFSET_Y + self.pacman_grid_y * self.current_cell_size
        )

    def find_42_pattern_cells(self) -> list[tuple[int, int]]:
        return [
            (x, y)
            for y, row in enumerate(self.current_maze)
            for x, _ in enumerate(row)
            # if cell is fully closed
            if self.current_maze[y][x] == 15
        ]

    def find_start_coords(self) -> tuple[int, int]:
        x = len(self.current_maze[0]) // 2
        y = len(self.current_maze) // 2
        if (x, y) not in self.fourty_two_cells:
            return (x, y)

        while (x, y) in self.fourty_two_cells:
            x -= 1

        return (x, y)

    def reset_level(self) -> None:
        self.current_maze = self.levels[self.current_level].maze.maze
        self.current_cell_size = self.levels[self.current_level].cell_size

        self.fourty_two_cells = self.find_42_pattern_cells()
        pacman_start_coords = self.find_start_coords()

        self.pacman_grid_x = pacman_start_coords[0]
        self.pacman_grid_y = pacman_start_coords[1]

        self.pacman_x = (
            self.MAZE_OFFSET_X + self.pacman_grid_x * self.current_cell_size
        )
        self.pacman_y = (
            self.MAZE_OFFSET_Y + self.pacman_grid_y * self.current_cell_size
        )

        pacman_start = (self.pacman_grid_x, self.pacman_grid_y)
        self.pacgums = set()
        for y, row in enumerate(self.current_maze):
            for x, _ in enumerate(row):
                if (x, y) not in self.fourty_two_cells and (
                    x,
                    y,
                ) != pacman_start:
                    self.pacgums.add((x, y))

        self.target_x = self.pacman_x
        self.target_y = self.pacman_y

        self.statistics = Statistics(config=self.config)
        self.level_timer = 0
