import pygame

from pacman.core import GameState
from pacman.ui import Colors


class MazeVisualMixin:
    def draw_wall(self, mask_value, x, y, cell_size, thickness, state) -> None:
        sprite = self.sprites.get_sprite_by_mask(
            mask_value, cell_size, thickness
        )

        wall_x = state.MAZE_OFFSET_X + x * cell_size
        wall_y = state.MAZE_OFFSET_Y + y * cell_size

        if mask_value in [8, 10, 12, 14]:
            wall_x -= thickness

        if mask_value in [1, 3, 5, 7]:
            wall_y -= thickness

        if mask_value in [9, 11, 13, 15]:
            wall_x -= thickness
            wall_y -= thickness

        self.screen.blit(sprite, (wall_x, wall_y))

    def get_mask_value(
        self, x: int, y: int, rows: int, cols: int, maze: list[list[int]]
    ) -> int:
        top_left_cell = maze[y - 1][x - 1] if y > 0 and x > 0 else None
        top_right_cell = maze[y - 1][x] if y > 0 and x < cols else None
        bottom_left_cell = maze[y][x - 1] if y < rows and x > 0 else None
        bottom_right_cell = maze[y][x] if y < rows and x < cols else None

        mask = 0

        # if vertical up wall
        if (top_left_cell and top_left_cell & 2) or (
            top_right_cell and top_right_cell & 8
        ):
            mask |= 1

        # if vertical down wall
        if (bottom_left_cell and bottom_left_cell & 2) or (
            bottom_right_cell and bottom_right_cell & 8
        ):
            mask |= 4

        # if horizontal left wall
        if (top_left_cell and top_left_cell & 4) or (
            bottom_left_cell and bottom_left_cell & 1
        ):
            mask |= 8

        # if horizontal right wall
        if (top_right_cell and top_right_cell & 4) or (
            bottom_right_cell and bottom_right_cell & 1
        ):
            mask |= 2

        return mask

    def draw_maze(self, state: GameState) -> None:
        # 1,2,4,8 = N, E, S, W
        maze = state.current_maze
        cell_size = state.current_cell_size

        # go through each cell of the maze
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                px = state.MAZE_OFFSET_X + x * cell_size
                py = state.MAZE_OFFSET_Y + y * cell_size

                # if cell of 42 pattern, 4 walls, closed
                if cell == 15:
                    pygame.draw.rect(
                        self.screen,
                        Colors.NEON_PINK.value,
                        (px, py, cell_size, cell_size),
                    )

        rows = len(maze)
        cols = len(maze[0])
        intersections_count_x = cols + 1
        intersections_count_y = rows + 1

        # go through every intersection of the maze
        for y in range(0, intersections_count_y):
            for x in range(0, intersections_count_x):

                mask_value = self.get_mask_value(x, y, rows, cols, maze)

                if mask_value == 0:
                    continue

                self.draw_wall(
                    mask_value, x, y, cell_size, state.wall_thickness, state
                )

                # dessiner le sprite correspondant au numero de mask

                # OLD VERSION

                # # top wall
                # if cell & 1:
                #     pygame.draw.line(
                #         self.screen,
                #         colors.WALL_BLUE.value,
                #         (px, py),
                #         (px + cell_size, py),
                #         self.radius(MAZE_WALL_WIDTH),
                #     )

                # # left wall
                # if cell & 8:
                #     pygame.draw.line(
                #         self.screen,
                #         colors.WALL_BLUE.value,
                #         (px, py),
                #         (px, py + cell_size),
                #         self.radius(MAZE_WALL_WIDTH),
                #     )

                # # right wall (last column)
                # if x == (cols - 1) and (cell & 2):
                #     pygame.draw.line(
                #         self.screen,
                #         colors.WALL_BLUE.value,
                #         (px + cell_size, py),
                #         (px + cell_size, py + cell_size),
                #         self.radius(MAZE_WALL_WIDTH),
                #     )

                # # bottom wall (last row)
                # if y == rows - 1 and (cell & 4):
                #     pygame.draw.line(
                #         self.screen,
                #         colors.WALL_BLUE.value,
                #         (px, py + cell_size),
                #         (px + cell_size, py + cell_size),
                #         self.radius(MAZE_WALL_WIDTH),
                #     )
