from typing import Any
from dataclasses import dataclass
from .statistics import Statistics
from .pacman_state import PacmanStateMixin
from .ghost_state import GhostStateMixin
from .level import Level


@dataclass(kw_only=True)
class GameState(PacmanStateMixin, GhostStateMixin):
    config: dict[str, Any]
    game: Any
    status: str = "pause"
    current_level_index: int = 0
    animation_timer: int = 0
    animation_delay: int = 100
    level_timer: int = 0

    def __post_init__(self):
        self.statistics = Statistics(config=self.config)
        self.reset_level()

    def get_level(self) -> Level:
        level = self.config["levels"][self.current_level_index]
        return Level(
            width=level["width"], height=level["height"], game=self.game
        )

    def find_42_pattern_cells(self) -> list[tuple[int, int]]:
        return [
            (x, y)
            for y, row in enumerate(self.current_maze)
            for x, _ in enumerate(row)
            # if cell is fully closed
            if self.current_maze[y][x] == 15
        ]

    def reset_level(self) -> None:
        self.status = "pause"

        self.level = self.get_level()
        self.current_maze = self.level.maze.maze
        self.fourty_two_cells = self.find_42_pattern_cells()

        self.update_level_layout()
        self.reset_pacman_state()
        self.reset_ghosts_states()

        self.level_timer = 0
        self.statistics.time_left = self.statistics.level_max_time

    def update_level_layout(self) -> None:
        self.level.cell_size = self.level._find_cell_size(
            self.level.width,
            self.level.height,
        )

        cell_size = self.level.cell_size

        self.wall_thickness = max(1, int(0.30 * cell_size))

        self.maze_width_pixel = self.level.width * cell_size

        self.maze_height_pixel = self.level.height * cell_size

        self.MAZE_OFFSET_X = self.game.black_rectangle_start[0] + (
            (self.game.black_rectangle_width - self.maze_width_pixel) // 2
        )
        self.MAZE_OFFSET_Y = self.game.black_rectangle_start[1] + (
            (self.game.black_rectangle_height - self.maze_height_pixel) // 2
        )

        last_row = self.level.height - 1
        last_col = self.level.width - 1

        self.maze_corners_coords = [
            (0, 0),
            (last_col, 0),
            (0, last_row),
            (last_col, last_row),
        ]

    def refresh_layout(self) -> None:
        self.update_level_layout()
        self.set_pacman_start_position()
