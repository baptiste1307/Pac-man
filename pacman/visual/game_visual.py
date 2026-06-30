import sys
import pygame
from dataclasses import dataclass
from pacman.ui import Button, Colors
from .menu_visual import MenuVisualMixin
from .maze_visual import MazeVisualMixin
from .play_visual import PlayVisualMixin
from .visual_base import VisualBaseMixin

DESIGN_SIZE = (2160, 1280)
INITIAL_WINDOW_SCALE = 0.7
PLAY_AREA_FILL_RATIO = 0.9

IMAGE_SIZES = {
    "white_frame": (1433, 871),
    "pacman_img": (1393, 929),
    "instruc_img": (170, 115),
    "type_name_img": (507, 221),
    "score_img": (436, 436),
    "score_board": (278, 278),
    "lives_icon": (149, 149),
    "level_icon": (149, 149),
    "timer_icon": (149, 149),
}

BUTTON_SPECS = {
    "start_button": (277, 86, 941, 721, "Start", (982, 726), 8),
    "instruction_button": (
        240,
        58,
        609,
        902,
        "Instruction",
        (626, 908),
        4,
    ),
    "score_button": (240, 58, 960, 902, "High Score", (988, 908), 4),
    "exit_button": (240, 58, 1311, 902, "Exit", (1390, 908), 4),
    "go_back_button": (160, 58, 1512, 912, "Go Back", (1523, 918), 2),
    "play_back_button": (160, 58, 1632, 1076, "Go Back", (1643, 1082), 2),
    "load_back_button": (240, 58, 960, 972, "Go Back", (1000, 978), 4),
    "next_level_button": (
        200,
        58,
        1832,
        1076,
        "Next Level",
        (1843, 1082),
        2,
    ),
}

FONT_SIZES = {
    "start_font": 64,
    "button_font": 36,
    "text_font": 24,
    "title_font": 48,
    "t_font": 32,
}

PLAY_AREA = {
    "start": (125, 140),
    "size": (1429, 1000),
}


@dataclass
class GameVisual(
    VisualBaseMixin,
    MenuVisualMixin,
    MazeVisualMixin,
    PlayVisualMixin,
):
    pygame.init()
    pygame.font.init()

    design_width = DESIGN_SIZE[0]
    design_height = DESIGN_SIZE[1]
    play_area_fill_ratio = PLAY_AREA_FILL_RATIO

    colors: type = Colors
    my_font: str = (
        "fonts/Bitcount_Prop_Double/BitcountPropDouble-VariableFont_"
        "CRSV,ELSH,ELXP,slnt,wght.ttf"
    )

    def __post_init__(self):
        info = pygame.display.Info()
        width = int(info.current_w * INITIAL_WINDOW_SCALE)
        height = int(info.current_h * INITIAL_WINDOW_SCALE)
        self.resize(width, height)
        self.assets = None
        self.sprites = None

    def fit_to_design_ratio(self, width: int, height: int) -> tuple[int, int]:
        width = max(1, width)
        height = max(1, height)
        design_ratio = self.design_width / self.design_height
        requested_ratio = width / height

        if requested_ratio > design_ratio:
            height = height
            width = int(height * design_ratio)
        else:
            width = width
            height = int(width / design_ratio)

        return max(1, width), max(1, height)

    def resize(self, width: int, height: int) -> None:
        self.screen_width, self.screen_height = self.fit_to_design_ratio(
            width, height
        )
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            pygame.RESIZABLE,
        )
        self.load_fonts()
        self.load_images()
        self.load_buttons()
        self.load_play_area()

    def font_size(self, value: int) -> int:
        return max(1, self.y(value))

    def load_fonts(self) -> None:
        for font_name, font_size in FONT_SIZES.items():
            setattr(
                self,
                font_name,
                pygame.font.Font(self.my_font, self.font_size(font_size)),
            )

    def load_images(self) -> None:
        self.background_img = pygame.transform.scale(
            pygame.image.load("./img/background.jpeg").convert(),
            (self.screen_width, self.screen_height),
        )
        self.white_frame = pygame.transform.scale(
            pygame.image.load("./img/white frame.png").convert_alpha(),
            self.size(IMAGE_SIZES["white_frame"]),
        )
        self.pacman_img = pygame.transform.scale(
            pygame.image.load("./img/pac-man-title.png").convert_alpha(),
            self.size(IMAGE_SIZES["pacman_img"]),
        )
        self.instruc_img = pygame.transform.scale(
            pygame.image.load("./img/keyboard.png").convert_alpha(),
            self.size(IMAGE_SIZES["instruc_img"]),
        )
        self.type_name_img = pygame.transform.scale(
            pygame.image.load("./img/type_name_img.png").convert_alpha(),
            self.size(IMAGE_SIZES["type_name_img"]),
        )
        self.score_img = pygame.transform.scale(
            pygame.image.load("./img/score_img.png").convert_alpha(),
            self.size(IMAGE_SIZES["score_img"]),
        )
        self.score_board = pygame.transform.scale(
            pygame.image.load("./img/play/score_board.png").convert_alpha(),
            self.size(IMAGE_SIZES["score_board"]),
        )
        self.lives_icon = pygame.transform.scale(
            pygame.image.load("./img/play/lives.png").convert_alpha(),
            self.size(IMAGE_SIZES["lives_icon"]),
        )
        self.level_icon = pygame.transform.scale(
            pygame.image.load("./img/play/level-badge.png").convert_alpha(),
            self.size(IMAGE_SIZES["level_icon"]),
        )
        self.timer_icon = pygame.transform.scale(
            pygame.image.load("./img/play/time.png").convert_alpha(),
            self.size(IMAGE_SIZES["timer_icon"]),
        )

    def make_button(
        self,
        width: int,
        height: int,
        x: int,
        y: int,
        text: str,
        text_pos: tuple[int, int],
        stroke_thickness: int,
    ) -> Button:
        return Button(
            self.x(width),
            self.y(height),
            self.x(x),
            self.y(y),
            text,
            self.pos(text_pos),
            self.x(stroke_thickness),
        )

    def load_buttons(self) -> None:
        for button_name, button_spec in BUTTON_SPECS.items():
            setattr(self, button_name, self.make_button(*button_spec))

    def load_play_area(self) -> None:
        self.black_rectangle_start = self.pos(PLAY_AREA["start"])
        self.black_rectangle_width = self.x(PLAY_AREA["size"][0])
        self.black_rectangle_height = self.y(PLAY_AREA["size"][1])

    def main_menu(self):
        page = "hero"
        scores = {"huian": 300, "baptiste": 600, "allan": 200}

        pygame.mixer.music.load("./sounds/background.ogg")
        pygame.mixer.music.play(-1)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.VIDEORESIZE:
                    self.resize(event.w, event.h)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    event_pos = event.pos
                    if page == "hero":
                        if pygame.Rect(self.start_button.rect).collidepoint(
                            event_pos
                        ):
                            page = "play"
                            # page = "loading"
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("./sounds/play_bgm.ogg")
                            pygame.mixer.music.set_volume(0.6)
                            pygame.mixer.music.play(-1)

                        if pygame.Rect(
                            self.instruction_button.rect
                        ).collidepoint(event_pos):
                            page = "instruction"
                        if pygame.Rect(self.score_button.rect).collidepoint(
                            event_pos
                        ):
                            page = "score"
                        if pygame.Rect(self.exit_button.rect).collidepoint(
                            event_pos
                        ):
                            sys.exit(0)
                    # elif page == "loading":
                    #     if pygame.Rect(self.load_back_button.rect
                    #                    ).collidepoint(
                    #         event_pos
                    #     ):
                    #         page = "hero"
                    elif page == "instruction":
                        if pygame.Rect(self.go_back_button.rect).collidepoint(
                            event_pos
                        ):
                            page = "hero"
                    elif page == "score":
                        if pygame.Rect(self.go_back_button.rect).collidepoint(
                            event_pos
                        ):
                            page = "hero"
                    elif page == "play":
                        if pygame.Rect(
                            self.play_back_button.rect
                        ).collidepoint(event_pos):
                            # Maybe need to stop game
                            # engine and then go back to hero?
                            page = "hero"
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("./sounds/background.ogg")
                            pygame.mixer.music.play(-1)
            if page == "hero":
                self.draw_hero()
            elif page == "loading":
                self.draw_load_game()
            elif page == "instruction":
                self.draw_instruction()
            elif page == "type_name":
                self.draw_type_name()
            elif page == "score":
                self.draw_score_list(scores)
            elif page == "play":
                return
            self.present()
        pygame.quit()


if __name__ == "__main__":
    v = GameVisual()
    v.main_menu()
