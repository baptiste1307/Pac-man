from dataclasses import dataclass
from typing import Any
from .shortest_path import find_shortest_path


@dataclass
class GhostState:
    state: Any
    asset_name: str
    direction: str
    grid_x: int
    grid_y: int
    pixel_x: int = 0
    pixel_y: int = 0
    pixel_target_x: int = 0
    pixel_target_y: int = 0

    def __post_init__(self):
        # self.last_pacman_coords = (
        #     self.state.pacman_grid_x,
        #     self.state.pacman_grid_y,
        # )

        self.pixel_x = (
            self.state.MAZE_OFFSET_X
            + (self.grid_x * self.state.level.cell_size)
            + self.state.wall_thickness
        )
        self.pixel_y = (
            self.state.MAZE_OFFSET_Y
            + (self.grid_y * self.state.level.cell_size)
            + self.state.wall_thickness
        )

        self.pixel_target_x = self.pixel_x
        self.pixel_target_y = self.pixel_y


@dataclass
class GhostStateMixin:
    ghost_current_frame: int = 0

    def reset_ghosts_states(self):

        self.ghost_speed = self.pacman_speed * 0.7
        last_col, last_row = self.level.width - 1, self.level.height - 1

        self.blinky = GhostState(self, "red_ghost", "right", 0, 0)
        self.pinky = GhostState(self, "pink_ghost", "left", last_col, 0)
        self.inky = GhostState(self, "blue_ghost", "right", 0, last_row)
        self.clyde = GhostState(
            self, "orange_ghost", "left", last_col, last_row
        )

    def update_ghosts_targets(self):
        self.update_blinky_target()

    # Blinky est sur une case grille
    # Pac-Man est sur une case grille
    # On calcule le plus court chemin entre les deux
    # On prend seulement la prochaine case du chemin
    # On met cette case comme target de Blinky

    def update_blinky_target(self):
        # if blinky is still moving to his target
        if (
            self.blinky.pixel_x != self.blinky.pixel_target_x
            or self.blinky.pixel_y != self.blinky.pixel_target_y
        ):
            return

        start = (self.blinky.grid_x, self.blinky.grid_y)
        goal = (self.pacman_grid_x, self.pacman_grid_y)

        path = find_shortest_path(self.current_maze, start, goal)

        if len(path) < 2:
            return

        next_cell = path[1]

        self.blinky.grid_x, self.blinky.grid_y = next_cell
        self.blinky.pixel_target_x = (
            self.MAZE_OFFSET_X
            + self.blinky.grid_x * self.level.cell_size
            + self.wall_thickness
        )
        self.blinky.pixel_target_y = (
            self.MAZE_OFFSET_Y
            + self.blinky.grid_y * self.level.cell_size
            + self.wall_thickness
        )
