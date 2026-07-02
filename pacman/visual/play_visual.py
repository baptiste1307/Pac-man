import pygame
from pacman.assets import LoadedAssets
from pacman.core import GameState
from pacman.ui import Colors

HUD_IMAGES_POS = {
    "score_board": (1632, 140),
    "lives_icon": (1632, 460),
    "level_icon": (1632, 623),
    "timer_icon": (1632, 802),
    "volume_bar": (1933, 1163),
    "game_over": (827, 120),
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
    "loading": (698, 848),
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
            self.score_board, self.pos(HUD_IMAGES_POS["score_board"])
        )
        self.draw_text(
            f"{state.statistics.score}",
            self.start_font,
            Colors.BLACK.value,
            HUD_TEXT_POSITIONS["score"],
            center=True,
        )

        self.screen.blit(
            self.lives_icon, self.pos(HUD_IMAGES_POS["lives_icon"])
        )
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

        self.screen.blit(
            self.level_icon, self.pos(HUD_IMAGES_POS["level_icon"])
        )
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
            f"{state.current_level_index + 1}",
            self.title_font,
            Colors.WHITE.value,
            HUD_TEXT_POSITIONS["level_value"],
        )

        self.screen.blit(
            self.timer_icon, self.pos(HUD_IMAGES_POS["timer_icon"])
        )
        self.draw_text(
            f"{state.statistics.time_left}",
            self.start_font,
            Colors.WHITE.value,
            HUD_TEXT_POSITIONS["timer"],
        )

        self.draw_button(self.play_back_button, self.button_font)
        self.draw_button(self.next_level_button, self.button_font)
        self.screen.blit(self.volume_bar, HUD_IMAGES_POS["volume_bar"])
        self.screen.blit(self.volume_knob, (self.knob_x, self.knob_y))

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

    def draw_grid_asset(
        self,
        state: GameState,
        asset_name: str,
        grid_position: tuple[int, int],
        sub_name: str | None = None,
        frame_index: int | None = None,
    ) -> None:
        cell_size = state.level.cell_size
        thickness = state.wall_thickness

        if self.assets is None:
            self.assets = LoadedAssets()

        asset = self.assets.get_asset(
            name=asset_name,
            cell_size=cell_size,
            sub_name=sub_name,
            thickness=thickness,
        )

        if isinstance(asset, list) and frame_index is not None:
            asset = asset[frame_index % len(asset)]

        asset_rect = asset.get_rect()
        x, y = grid_position

        if "pacman" in asset_name or "ghost" in asset_name:
            self.screen.blit(asset, grid_position)

        else:
            asset_rect.center = (
                state.MAZE_OFFSET_X
                + (x * cell_size)
                + thickness
                + ((cell_size - thickness) // 2),
                state.MAZE_OFFSET_Y
                + (y * cell_size)
                + thickness
                + ((cell_size - thickness) // 2),
            )

            self.screen.blit(asset, asset_rect)

    def draw_pacman(self, state: GameState) -> None:

        direction = state.pacman_direction or "right"
        x = state.pacman_x
        y = state.pacman_y

        if direction == "up":
            asset = "pacman_up"
        elif direction == "down":
            asset = "pacman_down"
        elif direction == "right":
            asset = "pacman_right"
        elif direction == "left":
            asset = "pacman_left"

        self.draw_grid_asset(
            state, asset, (x, y), "all", state.pacman_current_frame
        )

    def draw_pacgums(self, state: GameState) -> None:

        if len(state.pacgums) == 0 and len(state.super_pacgums) == 0:
            self.draw_good_job()
            state.current_level_index += 1
            state.reset_level()

        for x, y in state.pacgums:
            self.draw_grid_asset(state, "pacgum", (x, y))

        for x, y in state.super_pacgums:
            self.draw_grid_asset(state, "super_pacgum", (x, y))

    def draw_ghosts(self, state: GameState) -> None:
        if len(state.pacgums) == 0:
            state.current_level_index += 1
            state.reset_level()

        for ghost in state.ghosts:
            self.draw_grid_asset(
                state=state,
                asset_name=f"{ghost.asset_name}_{ghost.direction}",
                grid_position=(ghost.pixel_x, ghost.pixel_y),
                sub_name="all",
                frame_index=state.ghost_current_frame,
            )

    def draw_game_over(self):
        # game_over_sound = pygame.mixer.Sound("./sounds/congrats.mp3")
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))

        game_over_rect = self.game_over.get_rect(
            topleft=HUD_IMAGES_POS["game_over"]
        )

        self.screen.blit(self.game_over, game_over_rect)
        self.draw_button(self.play_back_button, self.button_font)
        # game_over_sound.play()
        # game_over_sound.set_volume(0.8)

    def draw_good_job(self):
        start_time = pygame.time.get_ticks()
        clock = pygame.time.Clock()
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        good_job_rect = self.good_job.get_rect(
            topleft=HUD_IMAGES_POS["game_over"]
        )

        while pygame.time.get_ticks() - start_time < 3000:
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(self.good_job, good_job_rect)
            self.draw_button(self.play_back_button, self.button_font)
            self.draw_text("Loading your next level...", self.title_font,
                           Colors.WHITE.value, HUD_TEXT_POSITIONS["loading"])

            delta_time = clock.tick(60) / 1000
            self.draw_loading_pacman(delta_time)
            pygame.display.flip()

    def draw_loading_pacman(self, dt):

        self.loading_frame += 1
        if (self.loading_frame // 10) % 2 == 0:
            self.screen.blit(self.loading_pacman1,
                             (self.current_point, self.loading_height))
        else:
            self.screen.blit(self.loading_pacman2,
                             (self.current_point, self.loading_height))
        if self.current_point < self.end_point:
            self.current_point += self.loading_speed * dt
        else:
            self.current_point = self.start_point
