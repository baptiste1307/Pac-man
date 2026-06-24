import pygame

from pacman.core import GameState
from pacman.ui import Colors


class PlayVisualMixin:
    def draw_play(self, state: GameState):
        score_board = pygame.transform.scale(
            pygame.image.load("./img/play/score_board.png").convert_alpha(),
            (278, 278),
        )
        lives_icon = pygame.transform.scale(
            pygame.image.load("./img/play/lives.png").convert_alpha(),
            (149, 149),
        )
        level_icon = pygame.transform.scale(
            pygame.image.load("./img/play/level-badge.png").convert_alpha(),
            (149, 149),
        )
        timer_icon = pygame.transform.scale(
            pygame.image.load("./img/play/time.png").convert_alpha(),
            (149, 149),
        )

        r_start_x, r_start_y = (
            self.black_rectangle_start[0],
            self.black_rectangle_start[1],
        )

        r_width, r_height = (
            self.black_rectangle_width,
            self.black_rectangle_height,
        )

        self.screen.blit(self.background_img, (0, 0))
        pygame.draw.rect(
            self.screen,
            Colors.BLACK.value,
            (r_start_x, r_start_y, r_width, r_height),
            border_radius=50,
        )
        self.screen.blit(score_board, (1632, 140))
        self.draw_text(
            f"{state.statistics.score}",
            self.start_font,
            Colors.BLACK.value,
            (1774, 323),
            center=True,
        )

        self.screen.blit(lives_icon, (1632, 460))
        pygame.draw.rect(
            self.screen,
            Colors.CYAN.value,
            (1632, 512, 149, 44),
            border_radius=8,
        )
        self.draw_text(
            "LIVES", self.button_font, Colors.BLACK.value, (1663, 516)
        )
        self.draw_text(
            f"{state.statistics.lives}",
            self.title_font,
            Colors.WHITE.value,
            (1833, 492),
        )

        self.screen.blit(level_icon, (1632, 623))
        pygame.draw.rect(
            self.screen,
            Colors.CYAN.value,
            (1632, 684, 149, 44),
            border_radius=8,
        )
        self.draw_text(
            "LEVEL", self.button_font, Colors.BLACK.value, (1658, 686)
        )
        self.draw_text(
            f"{state.current_level + 1}",
            self.title_font,
            Colors.WHITE.value,
            (1833, 683),
        )

        self.screen.blit(timer_icon, (1632, 802))
        self.draw_text(
            f"{state.statistics.time_left}",
            self.start_font,
            Colors.WHITE.value,
            (1833, 862),
        )

        self.draw_button(self.play_back_button, self.button_font)
        self.draw_button(self.next_level_button, self.button_font)

    # def draw_stats(self, state: GameState) -> None:

    #     font = pygame.font.SysFont("arial", 24)
    #     stats_x = 25
    #     stats_y = 5

    #     score_text = font.render(
    #         f"Score: {state.statistics.score}", True, self.colors.WHITE.value
    #     )

    #     lives_text = font.render(
    #         f"Lives: {state.statistics.lives}", True, self.colors.WHITE.value
    #     )

    #     level_text = font.render(
    #         f"Level: {state.current_level + 1}",
    #         True,
    #         self.colors.WHITE.value,
    #     )

    #     time_text = font.render(
    #         f"Time: {state.statistics.time_left}",
    #         True,
    #         self.colors.WHITE.value,
    #     )

    #     self.screen.blit(score_text, (stats_x, stats_y + 20))
    #     self.screen.blit(lives_text, (stats_x, stats_y + 40))
    #     self.screen.blit(level_text, (stats_x, stats_y + 60))
    #     self.screen.blit(time_text, (stats_x, stats_y + 80))

    def draw_pacman(self, state: GameState) -> None:

        direction = state.direction
        x = state.pacman_x
        y = state.pacman_y
        cell_size = state.current_cell_size
        current_frame = state.current_frame

        if direction == "up":
            asset = "pacman_up"
        elif direction == "down":
            asset = "pacman_down"
        elif direction == "right":
            asset = "pacman_right"
        elif direction == "left":
            asset = "pacman_left"

        pacman = self.assets.get_image(
            name=asset,
            sub_name="all",
            maze_cell_size=cell_size,
        )

        self.screen.blit(
            pacman[current_frame],
            # coordinates where to draw it
            (x, y),
        )

    def draw_pacgums(self, state: GameState) -> None:
        cell_size = state.current_cell_size

        dot = self.assets.get_image(name="dot", maze_cell_size=cell_size)

        dot_rect = dot.get_rect()

        if len(state.pacgums) == 0:
            state.current_level += 1
            state.reset_level()

        for x, y in state.pacgums:
            dot_rect.center = (
                state.MAZE_OFFSET_X + (x * cell_size) + (cell_size // 2),
                state.MAZE_OFFSET_Y + (y * cell_size) + (cell_size // 2),
            )

            self.screen.blit(dot, dot_rect)

    def draw_grid_asset(
        self,
        state: GameState,
        asset_name: str,
        grid_position: tuple[int, int],
        sub_name: str | None = None,
        frame_index: int | None = None,
    ) -> None:
        cell_size = state.current_cell_size

        asset = self.assets.get_image(
            name=asset_name,
            maze_cell_size=cell_size,
            sub_name=sub_name,
        )

        if isinstance(asset, list) and frame_index is not None:
            asset = asset[frame_index % len(asset)]

        asset_rect = asset.get_rect()
        x, y = grid_position

        asset_rect.center = (
            state.MAZE_OFFSET_X + (x * cell_size) + (cell_size // 2),
            state.MAZE_OFFSET_Y + (y * cell_size) + (cell_size // 2),
        )

        self.screen.blit(asset, asset_rect)

    def draw_ghosts(self, state: GameState) -> None:
        if len(state.pacgums) == 0:
            state.current_level += 1
            state.reset_level()

        maze = state.current_maze
        last_row = len(maze) - 1
        last_col = len(maze[0]) - 1

        ghosts_start_positions = {
            "red_ghost_right": (0, 0),
            "pink_ghost_left": (last_col, 0),
            "blue_ghost_right": (0, last_row),
            "orange_ghost_left": (last_col, last_row),
        }

        for ghost, position in ghosts_start_positions.items():
            self.draw_grid_asset(
                state=state,
                asset_name=ghost,
                grid_position=position,
                sub_name="all",
                frame_index=state.current_frame,
            )

    def draw_maze(self, state: GameState) -> None:
        # 1,2,4,8 = N, E, S, W
        colors = self.colors

        maze = state.current_maze
        cell_size = state.current_cell_size

        rows = len(maze)
        cols = len(maze[0])

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):

                px = state.MAZE_OFFSET_X + x * cell_size
                py = state.MAZE_OFFSET_Y + y * cell_size

                # top wall
                if cell & 1:
                    pygame.draw.line(
                        self.screen,
                        colors.WALL_BLUE.value,
                        (px, py),
                        (px + cell_size, py),
                        5,
                    )

                # left wall
                if cell & 8:
                    pygame.draw.line(
                        self.screen,
                        colors.WALL_BLUE.value,
                        (px, py),
                        (px, py + cell_size),
                        5,
                    )

                # right wall (last column)
                if x == (cols - 1) and (cell & 2):
                    pygame.draw.line(
                        self.screen,
                        colors.WALL_BLUE.value,
                        (px + cell_size, py),
                        (px + cell_size, py + cell_size),
                        5,
                    )

                # bottom wall (last row)
                if y == rows - 1 and (cell & 4):
                    pygame.draw.line(
                        self.screen,
                        colors.WALL_BLUE.value,
                        (px, py + cell_size),
                        (px + cell_size, py + cell_size),
                        5,
                    )
