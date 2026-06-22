import pygame
from typing import Any
from dataclasses import dataclass, field
<<<<<<< HEAD
from .visual_utils import Colors
from .assets import LoadedAssets
=======
from .visual_utils import Colors, Level, Button
from typing import Tuple
>>>>>>> hliu

MAZE_OFFSET_X = 25
MAZE_OFFSET_Y = 125


@dataclass
class GameVisual:
    pygame.init()
    pygame.font.init()

    screen_width: int = 2160
    screen_height: int = 1280
    screen: Any = pygame.display.set_mode((screen_width, screen_height))
    colors: type = Colors
    my_font: str = "fonts/Zen_Dots/ZenDots-Regular.ttf"

    # =================== Fonts =================== #

    # ------------------- Hero ------------------- #

    start_font = pygame.font.SysFont(my_font, 64)
    button_font = pygame.font.SysFont(my_font, 36)
    text_font = pygame.font.SysFont(my_font, 24)

    # =================== Images =================== #

    background_img = pygame.transform.scale(
        pygame.image.load("./img/background.jpeg").convert(),
        (screen_width, screen_height))

    # ------------------- Hero ------------------- #

    pacman_img = pygame.transform.scale(
        pygame.image.load("./img/pac-man-title.png").convert_alpha(),
        (1393, 929))

    # =================== Buttons =================== #

    # ------------------- Hero ------------------- #

    start_button = Button(911, 711, 277, 86, "start", (987, 745), 30)

    def __post_init__(self):
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )

    def draw_button(self, button: Button, button_font) -> None:
        mouse = pygame.mouse.get_pos()
        button_rect = (button.rect_pos_x, button.rect_pos_y,
                       button.rect_width, button.rect_height)

        hovered = pygame.Rect(button_rect).collidepoint(mouse)

        color = Colors.D_BLUE.value
        stroke_and_text_color = Colors.CYAN.value if hovered else Colors.B_YELLOW.value

        pygame.draw.rect(self.screen, color, button_rect,
                         border_radius=button.stroke_thickness)
        texto = button_font.render(button.text, True, stroke_and_text_color)
        self.screen.blit(texto, button.text_rect)

    def draw_loading():
        pass

    def draw_hero(self):
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.pacman_img, (383, 0))
        self.draw_button(self.start_button, self.start_font)

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

    def draw_pacman(self, cell_size: int):
        a = LoadedAssets()

        pacman = a.get_image(
            "pacman_right",
            "opened",
            cell_size,
        )

        self.screen.blit(
            pacman,
            # coordinates where to draw it
            (300, 300),
        )

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

            menu_text = {
                "title_text": {
                    "text": font.render("PAC-MAN", True, colors.YELLOW.value),
                    "y_pos": 150,
                },
                "start_text": {
                    "text": small_font.render(
                        "Press SPACE to start", True, colors.WHITE.value
                    ),
                    "y_pos": 300,
                },
                "quit_text": {
                    "text": small_font.render(
                        "Press ESC to quit", True, colors.WHITE.value
                    ),
                    "y_pos": 350,
                },
            }

            for data in menu_text.values():

                self.screen.blit(
                    data["text"],
                    (
                        self.screen.get_width() // 2
                        - data["text"].get_width() // 2,
                        data["y_pos"],
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

    def test_draw(self):
        page = "hero"

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if page == "hero":
                        pass

            self.draw_hero()
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    v = GameVisual()
    v.test_draw()
