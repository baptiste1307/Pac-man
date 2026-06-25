import pygame

from pacman.core import GameState
from pacman.ui import Colors

HUD_IMAGES = {
    "score_board": {"size": (278, 278), "pos": (1632, 140)},
    "lives_icon": {"size": (149, 149), "pos": (1632, 460)},
    "level_icon": {"size": (149, 149), "pos": (1632, 623)},
    "timer_icon": {"size": (149, 149), "pos": (1632, 802)},
}

HUD_LABEL_RECTS = {
    "lives": (1632, 512, 149, 44),
    "level": (1632, 684, 149, 44),
}

HUD_TEXT_POSITIONS = {
    "score": (1774, 323),
    "lives_label": (1663, 516),
    "lives_value": (1833, 492),
    "level_label": (1658, 686),
    "level_value": (1833, 683),
    "timer": (1833, 862),
}

NEXT_BUTTON = {
    "font_size": 24,
    "width": 120,
    "height": 50,
    "right_margin": 20,
    "top": 40,
}

MAZE_WALL_WIDTH = 5
PLAY_AREA_RADIUS = 50
HUD_LABEL_RADIUS = 8


class PlayVisualMixin:
    def draw_play(self, state: GameState):
        score_board = pygame.transform.scale(
            pygame.image.load("./img/play/score_board.png").convert_alpha(),
            self.size(HUD_IMAGES["score_board"]["size"]),
        )
        lives_icon = pygame.transform.scale(
            pygame.image.load("./img/play/lives.png").convert_alpha(),
            self.size(HUD_IMAGES["lives_icon"]["size"]),
        )
        level_icon = pygame.transform.scale(
            pygame.image.load("./img/play/level-badge.png").convert_alpha(),
            self.size(HUD_IMAGES["level_icon"]["size"]),
        )
        timer_icon = pygame.transform.scale(
            pygame.image.load("./img/play/time.png").convert_alpha(),
            self.size(HUD_IMAGES["timer_icon"]["size"]),
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
            border_radius=self.radius(PLAY_AREA_RADIUS),
        )
        self.screen.blit(
            score_board, self.pos(HUD_IMAGES["score_board"]["pos"])
        )
        self.draw_text(
            f"{state.statistics.score}",
            self.start_font,
            Colors.BLACK.value,
            HUD_TEXT_POSITIONS["score"],
            center=True,
        )

        self.screen.blit(lives_icon, self.pos(HUD_IMAGES["lives_icon"]["pos"]))
        pygame.draw.rect(
            self.screen,
            Colors.CYAN.value,
            self.rect(HUD_LABEL_RECTS["lives"]),
            border_radius=self.radius(HUD_LABEL_RADIUS),
        )
        self.draw_text(
            "LIVES",
            self.button_font,
            Colors.BLACK.value,
            HUD_TEXT_POSITIONS["lives_label"],
        )
        self.draw_text(
            f"{state.statistics.lives}",
            self.title_font,
            Colors.WHITE.value,
            HUD_TEXT_POSITIONS["lives_value"],
        )

        self.screen.blit(level_icon, self.pos(HUD_IMAGES["level_icon"]["pos"]))
        pygame.draw.rect(
            self.screen,
            Colors.CYAN.value,
            self.rect(HUD_LABEL_RECTS["level"]),
            border_radius=self.radius(HUD_LABEL_RADIUS),
        )
        self.draw_text(
            "LEVEL",
            self.button_font,
            Colors.BLACK.value,
            HUD_TEXT_POSITIONS["level_label"],
        )
        self.draw_text(
            f"{state.current_level + 1}",
            self.title_font,
            Colors.WHITE.value,
            HUD_TEXT_POSITIONS["level_value"],
        )

        self.screen.blit(timer_icon, self.pos(HUD_IMAGES["timer_icon"]["pos"]))
        self.draw_text(
            f"{state.statistics.time_left}",
            self.start_font,
            Colors.WHITE.value,
            HUD_TEXT_POSITIONS["timer"],
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

    # DEBUG (to delete)
    def draw_next_button(self) -> pygame.Rect:

        colors = self.colors

        font = pygame.font.SysFont("arial", self.y(NEXT_BUTTON["font_size"]))

        button_width = self.x(NEXT_BUTTON["width"])
        button_height = self.y(NEXT_BUTTON["height"])

        button_x = (
            self.screen.get_width()
            - button_width
            - self.x(NEXT_BUTTON["right_margin"])
        )
        button_y = self.y(NEXT_BUTTON["top"])

        button_rect = pygame.Rect(
            button_x, button_y, button_width, button_height
        )

        pygame.draw.rect(self.screen, colors.YELLOW.value, button_rect)

        text = font.render("NEXT", True, colors.BLACK.value)

        self.screen.blit(
            text,
            (
                button_rect.centerx - text.get_width() // 2,
                button_rect.centery - text.get_height() // 2,
            ),
        )

        return button_rect

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

                # if cell of 42 pattern, 4 walls, closed
                if cell == 15:  
                    pygame.draw.rect(
                        self.screen,
                        Colors.NEON_PINK.value,
                        (px, py, cell_size, cell_size)
                    )

                # top wall
                if cell & 1:
                    pygame.draw.line(
                        self.screen,
                        colors.WALL_BLUE.value,
                        (px, py),
                        (px + cell_size, py),
                        self.radius(5),
                        self.radius(MAZE_WALL_WIDTH),
                    )

                # left wall
                if cell & 8:
                    pygame.draw.line(
                        self.screen,
                        colors.WALL_BLUE.value,
                        (px, py),
                        (px, py + cell_size),
                        self.radius(5),
                        self.radius(MAZE_WALL_WIDTH),
                    )

                # right wall (last column)
                if x == (cols - 1) and (cell & 2):
                    pygame.draw.line(
                        self.screen,
                        colors.WALL_BLUE.value,
                        (px + cell_size, py),
                        (px + cell_size, py + cell_size),
                        self.radius(5),
                        self.radius(MAZE_WALL_WIDTH),
                    )

                # bottom wall (last row)
                if y == rows - 1 and (cell & 4):
                    pygame.draw.line(
                        self.screen,
                        colors.WALL_BLUE.value,
                        (px, py + cell_size),
                        (px + cell_size, py + cell_size),
                        self.radius(5),
                        self.radius(MAZE_WALL_WIDTH),
                    )
