import pygame
from typing import Any, Tuple, Dict
from dataclasses import dataclass
from .utils.visual_utils import Colors, Button
from .assets import LoadedAssets

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
    my_font: str = "fonts/Bitcount_Prop_Double/BitcountPropDouble-VariableFont_CRSV,ELSH,ELXP,slnt,wght.ttf"

    # =================== Fonts =================== #

    start_font = pygame.font.Font(my_font, 64)
    button_font = pygame.font.Font(my_font, 36)
    text_font = pygame.font.Font(my_font, 24)
   
    title_font = pygame.font.Font(my_font, 48)
    t_font = pygame.font.Font(my_font, 32)

    # =================== Images =================== #

    background_img = pygame.transform.scale(
        pygame.image.load("./img/background.jpeg").convert(),
        (screen_width, screen_height))
    white_frame = pygame.transform.scale(
        pygame.image.load("./img/white frame.png").convert_alpha(),
        (1433, 871))
    pacman_img = pygame.transform.scale(
        pygame.image.load("./img/pac-man-title.png").convert_alpha(),
        (1393, 929))
    instruc_img = pygame.transform.scale(
        pygame.image.load("./img/keyboard.png").convert_alpha(),
        (170, 115))
    type_name_img = pygame.transform.scale(
        pygame.image.load("./img/type_name_img.png").convert_alpha(),
        (507, 221))
    score_img = pygame.transform.scale(
        pygame.image.load("./img/score_img.png").convert_alpha(),
        (436, 436))
    

    # =================== Buttons =================== #

    start_button = Button(277, 86, 941, 721, "Start", (982, 726), 8)
    instruction_button = Button(240, 58, 609, 902, "Instruction", (626, 908), 4)
    score_button = Button(240, 58, 960, 902, "High Score", (988, 908), 4)
    exit_button = Button(240, 58, 1311, 902, "Exit", (1390, 908), 4)
    go_back_button = Button(160, 58, 1512, 912, "Go Back", (1523, 918), 2)
    play_back_button = Button(160, 58, 1632, 1076, "Go Back", (1643, 1082), 2)

    def __post_init__(self):
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )

    # =================== Basic Methods =================== #

    def draw_button(self, button: Button, button_font) -> None:
        mouse = pygame.mouse.get_pos()
        stroke_rect = (
            button.rect_pos_x,
            button.rect_pos_y,
            button.rect_width,
            button.rect_height
        )
        button_rect = (
            button.rect_pos_x + button.stroke_thickness,
            button.rect_pos_y + button.stroke_thickness,
            button.rect_width - 2 * button.stroke_thickness,
            button.rect_height - 2 * button.stroke_thickness
        )
        shade_rect = (
            button.rect_pos_x,
            button.rect_pos_y + button.stroke_thickness,
            button.rect_width,
            button.rect_height
        )

        hovered = pygame.Rect(stroke_rect).collidepoint(mouse)

        button_color = Colors.D_BLUE.value
        stroke_and_text_color = (
            Colors.CYAN.value if hovered else Colors.B_YELLOW.value
        )
        texto = button_font.render(button.text, True, stroke_and_text_color)

        if not hovered:
            pygame.draw.rect(self.screen, Colors.CYAN.value, shade_rect,
                             border_radius=40)
            pygame.draw.rect(self.screen,
                    stroke_and_text_color,
                    stroke_rect,
                    border_radius=40)

        elif hovered:
            pygame.draw.rect(
                self.screen,
                stroke_and_text_color,
                stroke_rect,
                border_radius=40
            )     
        
        pygame.draw.rect(
            self.screen,
            button_color,
            button_rect,
            border_radius=30
        )

        if hovered:
            self.screen.blit(texto, (
                button.text_rect[0], button.text_rect[1] + 5))
        elif not hovered:
            self.screen.blit(texto, button.text_rect)
    
    def draw_text(self, text: str, font: Any,
                  color: Tuple[int, int, int], pos: Tuple[int, int],
                  center=False) -> None:
        """
        Draw text on the screen.

        Args:
            text: the text content to draw.
            font: the desired text font.
            color: the desired text color.
            pos: the position to draw the text.
            center: if the text is center-positioned (or topleft).
        """
        to_draw_text = font.render(text, True, color)
        if center:
            rect = to_draw_text.get_rect(center=pos)
            self.screen.blit(to_draw_text, rect)
        else:
            self.screen.blit(to_draw_text, pos)

    # =================== Pages Rendering =================== #

    def draw_loading():
        pass

    def draw_hero(self) -> None:
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.pacman_img, (383, 0))
        self.draw_button(self.start_button, self.start_font)
        self.draw_button(self.instruction_button, self.button_font)
        self.draw_button(self.score_button, self.button_font)
        self.draw_button(self.exit_button, self.button_font)
        self.draw_text("A lovely project by bpasquer & hliu", self.text_font, Colors.B_YELLOW.value, (875, 1094))

    def draw_instruction(self) -> None:
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.white_frame, (365, 208))
        pygame.draw.rect(self.screen, Colors.WHITE.value, (401, 258, 1356, 778), border_radius=30)
        self.draw_text("Instruction", self.title_font, Colors.D_BLUE.value, (461, 298))
        self.draw_text("Try not to get eaten by aggressive ghosts.\nYou will be moved to next level if you last", self.t_font, Colors.D_BLUE.value, (700, 402))
        self.draw_text("60 seconds!", self.t_font, Colors.RED.value, (1400, 440))
        self.draw_text("Use the arrow keys to move Pac-Man ", self.t_font, Colors.D_BLUE.value, (700, 534))
        self.draw_text("up, down", self.t_font, Colors.RED.value, (1307, 534))
        self.draw_text("left, and right ", self.t_font, Colors.RED.value, (700, 572))
        self.draw_text("inside the mize.", self.t_font, Colors.D_BLUE.value, (950, 572))
        self.draw_text("Small dot (pac-gum) = \nBig dot (super-gum) = \nAfter eating super-gum, ghosts become vulnerable, \nIt's time to eat them up! Each ghost = ", self.t_font, Colors.D_BLUE.value, (700, 666))
        self.draw_text("point,", self.t_font, Colors.D_BLUE.value, (1115, 666))
        self.draw_text("point,", self.t_font, Colors.D_BLUE.value, (1115, 704))
        self.draw_text("point,", self.t_font, Colors.D_BLUE.value, (1412, 780))
        self.draw_text("10", self.t_font, Colors.RED.value, (1070, 666))
        self.draw_text("50", self.t_font, Colors.RED.value, (1068, 704))
        self.draw_text("200", self.t_font, Colors.RED.value, (1346, 780))
        self.draw_text("Try to survive and collect as many points!\nHave fun!!",
                       self.t_font, Colors.D_BLUE.value, (700, 874))
        
        self.screen.blit(self.instruc_img, (461, 503))
        self.draw_button(self.go_back_button, self.button_font)

    def draw_type_name(self) -> None:
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.white_frame, (365, 208))
        pygame.draw.rect(self.screen, Colors.WHITE.value, (401, 258, 1356, 778), border_radius=30)
        self.draw_text("Congratulations !!!", self.start_font, Colors.D_BLUE.value, (779, 322))
        self.draw_text("Let us know what your name is...", self.title_font, Colors.D_BLUE.value, (681, 436))
        self.draw_text("__________", self.title_font, Colors.D_BLUE.value, (938, 531))
        self.screen.blit(self.type_name_img, (828, 678))
        self.draw_button(self.go_back_button, self.button_font)

    def draw_score_list(self, scores: Dict[str, int]) -> None:
        offset = 55
        nb_dashes = {}
        sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.white_frame, (365, 208))
        pygame.draw.rect(self.screen, Colors.WHITE.value, (401, 258, 1356, 778), border_radius=30)
        self.draw_text("Here are the best players...", self.title_font, Colors.D_BLUE.value, (743, 348))
        for name in scores.keys():
            total = 17
            nb_dash = total - len(name)
            nb_dashes[name] = nb_dash
        i = 0
        for name, score in sorted_scores.items():
            self.draw_text(f"{name} {'-' * nb_dashes[name]}",
                           self.button_font, Colors.D_BLUE.value,
                           (743, 434 + offset * i))
            self.draw_text(f"{score}", self.button_font, Colors.D_BLUE.value,
                           (1069, 434 + offset * i))
            i += 1
        self.screen.blit(self.score_img, (1208, 460))
        self.draw_button(self.go_back_button, self.button_font)

    def draw_play(self, level: int, lives: int, rest_time: int, score: int):
        score_board = pygame.transform.scale(
            pygame.image.load("./img/play/score_board.png").convert_alpha(),
            (278, 278))
        lives_icon = pygame.transform.scale(
            pygame.image.load("./img/play/lives.png").convert_alpha(),
            (149, 149))
        level_icon = pygame.transform.scale(
            pygame.image.load("./img/play/level-badge.png").convert_alpha(),
            (149, 149))
        timer_icon = pygame.transform.scale(
            pygame.image.load("./img/play/time.png").convert_alpha(),
            (149, 149))

        self.screen.blit(self.background_img, (0, 0))
        pygame.draw.rect(self.screen, Colors.BLACK.value, (125, 140, 1429, 1000), border_radius=50)
        self.screen.blit(score_board, (1632, 140))
        self.draw_text(f"{score}", self.start_font, Colors.BLACK.value, (1774, 323), center=True)
        
        self.screen.blit(lives_icon, (1632, 460))
        pygame.draw.rect(self.screen, Colors.CYAN.value, (1632, 512, 149, 44), border_radius=8)
        self.draw_text("LIVES", self.button_font, Colors.BLACK.value, (1663, 516))
        self.draw_text(f"{lives}", self.title_font, Colors.WHITE.value, (1833, 492))

        self.screen.blit(level_icon, (1632, 623))
        pygame.draw.rect(self.screen, Colors.CYAN.value, (1632, 684, 149, 44), border_radius=8)
        self.draw_text("LEVEL", self.button_font, Colors.BLACK.value, (1658, 686))
        self.draw_text(f"{level}", self.title_font, Colors.WHITE.value, (1833, 683))

        self.screen.blit(timer_icon, (1632, 802))
        self.draw_text(f"{rest_time}", self.start_font, Colors.WHITE.value, (1833, 862))

        self.draw_button(self.play_back_button, self.button_font)

        


    def test_draw(self):
        page = "hero"
        scores = {"huian": 300, "baptiste": 600, "allan": 200}

        running = True
        data = [1, 3, 60, 234]
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if page == "hero":
                        if pygame.Rect(self.start_button.rect
                                       ).collidepoint(event.pos):
                            page = "play"
                        if pygame.Rect(self.instruction_button.rect
                                       ).collidepoint(event.pos):
                            page = "instruction"
                        if pygame.Rect(self.score_button.rect
                                       ).collidepoint(event.pos):
                            page = "score"
                        if pygame.Rect(self.exit_button.rect
                                       ).collidepoint(event.pos):
                            running = False
                    elif page == "instruction":
                        if pygame.Rect(self.go_back_button.rect
                                       ).collidepoint(event.pos):
                            page = "hero"
                    elif page == "score":
                        if pygame.Rect(self.go_back_button.rect
                                       ).collidepoint(event.pos):
                            page = "hero"
                    elif page == "play":
                        if pygame.Rect(self.play_back_button.rect
                                       ).collidepoint(event.pos):
                            page = "hero"
            if page == "hero":
                self.draw_hero()
            elif page == "instruction":
                self.draw_instruction()
            elif page == "type_name":
                self.draw_type_name()
            elif page == "score":
                self.draw_score_list(scores)
            elif page == "play":
                self.draw_play(data[0], data[1], data[2], data[3])
            pygame.display.flip()
        pygame.quit()



















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

    def draw_pacman(
        self,
        direction: str,
        x: int,
        y: int,
        cell_size: int,
        assets: LoadedAssets,
        current_frame: int = 0,
    ) -> None:

        if direction == "up":
            asset = "pacman_up"
        elif direction == "down":
            asset = "pacman_down"
        elif direction == "right":
            asset = "pacman_right"
        elif direction == "left":
            asset = "pacman_left"

        pacman = assets.get_image(
            asset,
            "all",
            cell_size,
        )

        self.screen.blit(
            pacman[current_frame],
            # coordinates where to draw it
            (x, y),
        )

    def draw_maze(
        self,
        maze: list[list[int]],
        cell_size: int,
    ) -> None:
        # 1,2,4,8 = N, E, S, W
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


if __name__ == "__main__":
    v = GameVisual()
    v.test_draw()
