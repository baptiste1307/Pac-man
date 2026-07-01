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
    start_x: int | None = None
    start_y: int | None = None
    mode: str | None = None

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

        # only for clyde which moves back and forth between Pac-Man
        # and its starting point.
        if self.asset_name == "orange_ghost":
            self.start_x = self.grid_x
            self.start_y = self.grid_y
            # "chase" or "scatter"
            self.mode = "chase"


@dataclass
class GhostStateMixin:
    ghost_current_frame: int = 0

    def reset_ghosts_states(self):

        self.ghost_speed = self.pacman_speed * 0.5
        last_col, last_row = self.level.width - 1, self.level.height - 1

        self.blinky = GhostState(self, "red_ghost", "right", 0, 0)
        self.pinky = GhostState(self, "pink_ghost", "left", last_col, 0)
        self.inky = GhostState(self, "blue_ghost", "right", 0, last_row)
        self.clyde = GhostState(
            self, "orange_ghost", "left", last_col, last_row
        )
        self.ghosts = [self.blinky, self.pinky, self.clyde, self.inky]

    def update_ghosts_targets(self):

        # Blinky est sur une case grille
        # Pac-Man est sur une case grille
        # On calcule le plus court chemin entre les deux
        # On prend seulement la prochaine case du chemin
        # On met cette case comme target de Blinky

        for ghost in self.ghosts:
            # if ghost is still moving to his target
            if (
                ghost.pixel_x != ghost.pixel_target_x
                or ghost.pixel_y != ghost.pixel_target_y
            ):
                continue

            start = (ghost.grid_x, ghost.grid_y)
            if ghost == self.blinky:
                # blinky's target is pacman
                goal = (self.pacman_grid_x, self.pacman_grid_y)
            elif ghost == self.pinky:
                # pinky's target is a few cells around pacman
                goal = self.find_goal_near_pacman(self.pinky)
            elif ghost == self.clyde:
                # clyde's target alternates between pacman (chase mode)
                # and his starting point (scatter mode)
                goal = self.find_clyde_goal()
            elif ghost == self.inky:
                # inky's position is the opposite of blinky's one
                goal = self.find_inky_goal()

            path = find_shortest_path(self.current_maze, start, goal)

            if len(path) < 2:
                continue

            next_cell = path[1]

            ghost.grid_x, ghost.grid_y = next_cell
            ghost.pixel_target_x = (
                self.MAZE_OFFSET_X
                + ghost.grid_x * self.level.cell_size
                + self.wall_thickness
            )
            ghost.pixel_target_y = (
                self.MAZE_OFFSET_Y
                + ghost.grid_y * self.level.cell_size
                + self.wall_thickness
            )

    def find_goal_near_pacman(self, ghost):
        offset = 2

        if self.pacman_direction == "right":
            return (self.pacman_grid_x + offset, self.pacman_grid_y)
        if self.pacman_direction == "left":
            return (self.pacman_grid_x - offset, self.pacman_grid_y)
        if self.pacman_direction == "down":
            return (self.pacman_grid_x, self.pacman_grid_y + offset)
        if self.pacman_direction == "up":
            return (self.pacman_grid_x, self.pacman_grid_y - offset)

        return (self.pacman_grid_x, self.pacman_grid_y)

    def update_clyde_mode(self):
        clyde_pos = (self.clyde.grid_x, self.clyde.grid_y)
        pacman_pos = (self.pacman_grid_x, self.pacman_grid_y)
        corner_pos = (self.clyde.start_x, self.clyde.start_y)

        distance_to_pacman = abs(clyde_pos[0] - pacman_pos[0]) + abs(
            clyde_pos[1] - pacman_pos[1]
        )

        if self.clyde.mode == "chase" and distance_to_pacman <= 2:
            self.clyde.mode = "scatter"

        elif self.clyde.mode == "scatter" and clyde_pos == corner_pos:
            self.clyde.mode = "chase"

    def find_clyde_goal(self):
        self.update_clyde_mode()

        if self.clyde.mode == "scatter":
            return (self.clyde.start_x, self.clyde.start_y)

        return self.find_goal_near_pacman(self.clyde)

    def find_inky_goal(self):
        offset = 2

        ahead_x = self.pacman_grid_x
        ahead_y = self.pacman_grid_y

        if self.pacman_direction == "right":
            ahead_x += offset
        elif self.pacman_direction == "left":
            ahead_x -= offset
        elif self.pacman_direction == "down":
            ahead_y += offset
        elif self.pacman_direction == "up":
            ahead_y -= offset

        goal = (
            2 * ahead_x - self.blinky.grid_x,
            2 * ahead_y - self.blinky.grid_y,
        )

        return self.clamp_goal(goal)

    def clamp_goal(self, goal):
        """pour être sur que le goal ne dépasse pas les limites du maze"""
        x, y = goal
        x = max(0, min(x, self.level.width - 1))
        y = max(0, min(y, self.level.height - 1))
        return (x, y)
