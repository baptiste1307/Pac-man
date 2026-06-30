from dataclasses import dataclass


@dataclass
class PacmanStateMixin:
    pacman_speed: int = 3
    direction: str | None = None
    wanted_direction: str | None = None

    def update_target_position(self) -> None:
        self.target_x = (
            self.MAZE_OFFSET_X
            + self.pacman_grid_x * self.current_cell_size
            + self.wall_thickness
        )

        self.target_y = (
            self.MAZE_OFFSET_Y
            + self.pacman_grid_y * self.current_cell_size
            + self.wall_thickness
        )

    def find_start_coords(self) -> tuple[int, int]:
        x = len(self.current_maze[0]) // 2
        y = len(self.current_maze) // 2
        if (x, y) not in self.fourty_two_cells:
            return (x, y)

        while (x, y) in self.fourty_two_cells:
            x -= 1

        return (x, y)

    def reset_pacman_state(self):
        self.direction = None
        self.wanted_direction = None
        pacman_start_coords = self.find_start_coords()

        self.pacman_grid_x = pacman_start_coords[0]
        self.pacman_grid_y = pacman_start_coords[1]

        self.pacman_x = (
            self.MAZE_OFFSET_X
            + self.pacman_grid_x * self.current_cell_size
            + self.wall_thickness
        )
        self.pacman_y = (
            self.MAZE_OFFSET_Y
            + self.pacman_grid_y * self.current_cell_size
            + self.wall_thickness
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

    def set_pacman_start_position(self):
        self.pacman_x = (
            self.MAZE_OFFSET_X + self.pacman_grid_x * self.current_cell_size
        )
        self.pacman_y = (
            self.MAZE_OFFSET_Y + self.pacman_grid_y * self.current_cell_size
        )
        self.target_x = self.pacman_x
        self.target_y = self.pacman_y
