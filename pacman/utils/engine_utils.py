import pygame
from .visual_utils import Level
from typing import Any
from dataclasses import dataclass
from pacman.game_stats import GameStats


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

        self.statistics = GameStats(config=self.config)


class EngineUtils:
    def can_move(
        self,
        maze: list[list[int]],
        grid_x: int,
        grid_y: int,
        direction: str,
    ) -> bool:
        cell = maze[grid_y][grid_x]

        if direction == "up":
            return not (cell & 1)
        if direction == "right":
            return not (cell & 2)
        if direction == "down":
            return not (cell & 4)
        if direction == "left":
            return not (cell & 8)

        return False

    def next_level(self, state: GameState) -> None:
        state.current_level += 1

        if state.current_level >= len(state.levels):
            state.current_level = 0

        state.reset_level()

    def update_direction(self, state: GameState) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            state.direction = "left"
        elif keys[pygame.K_RIGHT]:
            state.direction = "right"
        elif keys[pygame.K_UP]:
            state.direction = "up"
        elif keys[pygame.K_DOWN]:
            state.direction = "down"

    def update_animation(self, state: GameState, dt: int) -> None:
        state.animation_timer += dt

        if state.animation_timer >= state.animation_delay:
            state.animation_timer = 0
            state.current_frame = (state.current_frame + 1) % 3

    def update_pacman_target(self, state: GameState) -> None:
        if (
            state.pacman_x != state.target_x
            or state.pacman_y != state.target_y
        ):
            return

        if not self.can_move(
            state.current_maze,
            state.pacman_grid_x,
            state.pacman_grid_y,
            state.direction,
        ):
            state.current_frame = 1
            return

        if state.direction == "up":
            state.pacman_grid_y -= 1
        elif state.direction == "right":
            state.pacman_grid_x += 1
        elif state.direction == "down":
            state.pacman_grid_y += 1
        elif state.direction == "left":
            state.pacman_grid_x -= 1

        current_cell = (state.pacman_grid_x, state.pacman_grid_y)

        if current_cell in state.pacgums:
            state.pacgums.remove(current_cell)
            state.statistics.score += state.config["points_per_pacgum"]

        state.update_target_position()

    def move_pacman(self, state: GameState) -> None:
        if state.pacman_x < state.target_x:
            state.pacman_x = min(
                state.pacman_x + state.pacman_speed,
                state.target_x,
            )
        elif state.pacman_x > state.target_x:
            state.pacman_x = max(
                state.pacman_x - state.pacman_speed,
                state.target_x,
            )

        if state.pacman_y < state.target_y:
            state.pacman_y = min(
                state.pacman_y + state.pacman_speed,
                state.target_y,
            )
        elif state.pacman_y > state.target_y:
            state.pacman_y = max(
                state.pacman_y - state.pacman_speed,
                state.target_y,
            )
