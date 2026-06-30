from dataclasses import dataclass


@dataclass
class PacmanStateMixin:
    pacman_speed: int = 1.5
    pacman_direction: str | None = None
    pacman_wanted_direction: str | None = None
    pacman_current_frame: int = 1

    def update_target_position(self) -> None:
        self.target_x = (
            self.MAZE_OFFSET_X
            + self.pacman_grid_x * self.level.cell_size
            + self.wall_thickness
        )

        self.target_y = (
            self.MAZE_OFFSET_Y
            + self.pacman_grid_y * self.level.cell_size
            + self.wall_thickness
        )

    def find_start_coords(self) -> tuple[int, int]:
        x = self.level.width // 2
        y = self.level.height // 2
        if (x, y) not in self.fourty_two_cells:
            return (x, y)

        while (x, y) in self.fourty_two_cells:
            x -= 1

        return (x, y)

    def reset_pacman_state(self):
        self.pacman_direction = None
        self.pacman_wanted_direction = None
        pacman_start_coords = self.find_start_coords()

        self.pacman_grid_x = pacman_start_coords[0]
        self.pacman_grid_y = pacman_start_coords[1]

        self.pacman_x = (
            self.MAZE_OFFSET_X
            + self.pacman_grid_x * self.level.cell_size
            + self.wall_thickness
        )
        self.pacman_y = (
            self.MAZE_OFFSET_Y
            + self.pacman_grid_y * self.level.cell_size
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
                    if len(self.pacgums) < 1:
                        self.pacgums.add((x, y))

        self.target_x = self.pacman_x
        self.target_y = self.pacman_y

    def set_pacman_start_position(self):
        self.pacman_x = (
            self.MAZE_OFFSET_X + self.pacman_grid_x * self.level.cell_size
        )
        self.pacman_y = (
            self.MAZE_OFFSET_Y + self.pacman_grid_y * self.level.cell_size
        )
        self.target_x = self.pacman_x
        self.target_y = self.pacman_y
