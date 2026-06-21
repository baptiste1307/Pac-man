import pygame
from typing import Any
from dataclasses import dataclass, field
from .visual_utils import Colors, Level

MAZE_OFFSET_X = 25
MAZE_OFFSET_Y = 125


@dataclass
class Visual:
    screen_width: int = 2160
    screen_height: int = 1280
    screen: Any = field(init=False)
    colors: type = Colors

    def __post_init__(self):
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )

    def draw_stats(
        self,
        config: dict[str, Any],
        current_level: int,
    ) -> None:

        colors = self.colors

        font = pygame.font.SysFont("arial", 24)
        stats_x = 25
        stats_y = 5

        game_score = 0

        score_text = font.render(
            f"Score: {game_score}", True, colors.WHITE.value
        )

        lives_text = font.render(
            f"Lives: {config['lives']}", True, colors.WHITE.value
        )

        level_text = font.render(
            f"Level: {current_level + 1}", True, colors.WHITE.value
        )

        time_text = font.render(
            f"Time: {config['level_max_time']}", True, colors.WHITE.value
        )

        self.screen.blit(score_text, (stats_x, stats_y + 20))
        self.screen.blit(lives_text, (stats_x, stats_y + 40))
        self.screen.blit(level_text, (stats_x, stats_y + 60))
        self.screen.blit(time_text, (stats_x, stats_y + 80))

    # DEBUG (to delete)
    def draw_next_button(self) -> pygame.Rect:

        colors = self.colors

        font = pygame.font.SysFont("arial", 24)

        button_width = 120
        button_height = 50

        button_x = self.screen.get_width() - button_width - 20
        button_y = 40

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

    def load_pacman(
        self,
        maze: list[list[int]],
        cell_size: int,
    ):
        # convert_alpha: for png with transparent bg & better performances
        return pygame.image.load("assets/pacman-right/1.png").convert_alpha()

    def draw_maze(
        self,
        maze: list[list[int]],
        cell_size: int,
    ) -> None:

        colors = self.colors

        rows = len(maze)
        cols = len(maze[0])

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):

                px = MAZE_OFFSET_X + x * cell_size
                py = MAZE_OFFSET_Y + y * cell_size

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

    def main_menu(self) -> None:

        colors = self.colors

        font = pygame.font.SysFont("arial", 48)
        small_font = pygame.font.SysFont("arial", 24)

        running = True

        while running:
            self.screen.fill(colors.BLACK.value)

            title_text = font.render("PAC-MAN", True, colors.YELLOW.value)

            start_text = small_font.render(
                "Press SPACE to start", True, colors.WHITE.value
            )

            quit_text = small_font.render(
                "Press ESC to quit", True, colors.WHITE.value
            )

            self.screen.blit(
                title_text,
                (
                    self.screen.get_width() // 2 - title_text.get_width() // 2,
                    150,
                ),
            )

            self.screen.blit(
                start_text,
                (
                    self.screen.get_width() // 2 - start_text.get_width() // 2,
                    300,
                ),
            )

            self.screen.blit(
                quit_text,
                (
                    self.screen.get_width() // 2 - quit_text.get_width() // 2,
                    350,
                ),
            )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

    def get_levels(self, config: dict[str, Any]) -> list[Level]:
        levels: list[Level] = []

        for level in config["levels"]:
            new_level = Level(width=level["width"], height=level["height"])
            levels.append(new_level)

        return levels

    def init_game(self, config: dict[str, Any]) -> None:

        pygame.init()
        levels = self.get_levels(config)

        pygame.display.set_caption("Pac-Man")

        self.main_menu()
        current_level = 0

        clock = pygame.time.Clock()
        running = True

        while running:
            next_button = self.draw_next_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if next_button.collidepoint(mouse_pos):
                        current_level += 1

                        if current_level >= len(levels):
                            current_level = 0

            self.screen.fill(self.colors.BLACK.value)

            self.draw_stats(config, current_level)

            self.draw_maze(
                levels[current_level].maze.maze,
                levels[current_level].cell_size,
            )

            self.screen.blit(
                # function to load pacman
                self.load_pacman(
                    levels[current_level].maze.maze,
                    levels[current_level].cell_size,
                ),
                # coordinates where to draw it
                (300, 300),
            )

            next_button = self.draw_next_button()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
