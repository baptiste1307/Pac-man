import pygame
from typing import Any
from dataclasses import dataclass
from pacman.assets import LoadedAssets
from pacman.ui import Button, Colors
from .menu_visual import MenuVisualMixin
from .play_visual import PlayVisualMixin
from .visual_base import VisualBaseMixin


@dataclass
class GameVisual(VisualBaseMixin, MenuVisualMixin, PlayVisualMixin):
    pygame.init()
    pygame.font.init()

    # adapt screen dimensions to be 70% of current display dimensions
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w * 0.7, info.current_h * 0.7

    screen: Any = pygame.display.set_mode((screen_width, screen_height))
    colors: type = Colors
    my_font: str = (
        "fonts/Bitcount_Prop_Double/BitcountPropDouble-VariableFont_"
        "CRSV,ELSH,ELXP,slnt,wght.ttf"
    )
    assets = LoadedAssets()

    # =================== Fonts =================== #

    start_font = pygame.font.Font(my_font, 64)
    button_font = pygame.font.Font(my_font, 36)
    text_font = pygame.font.Font(my_font, 24)

    title_font = pygame.font.Font(my_font, 48)
    t_font = pygame.font.Font(my_font, 32)

    # =================== Images =================== #

    background_img = pygame.transform.scale(
        pygame.image.load("./img/background.jpeg").convert(),
        (screen_width, screen_height),
    )
    white_frame = pygame.transform.scale(
        pygame.image.load("./img/white frame.png").convert_alpha(), (1433, 871)
    )
    pacman_img = pygame.transform.scale(
        pygame.image.load("./img/pac-man-title.png").convert_alpha(),
        (1393, 929),
    )
    instruc_img = pygame.transform.scale(
        pygame.image.load("./img/keyboard.png").convert_alpha(), (170, 115)
    )
    type_name_img = pygame.transform.scale(
        pygame.image.load("./img/type_name_img.png").convert_alpha(),
        (507, 221),
    )
    score_img = pygame.transform.scale(
        pygame.image.load("./img/score_img.png").convert_alpha(), (436, 436)
    )

    # =================== Buttons =================== #

    start_button = Button(277, 86, 941, 721, "Start", (982, 726), 8)
    instruction_button = Button(
        240, 58, 609, 902, "Instruction", (626, 908), 4
    )
    score_button = Button(240, 58, 960, 902, "High Score", (988, 908), 4)
    exit_button = Button(240, 58, 1311, 902, "Exit", (1390, 908), 4)
    go_back_button = Button(160, 58, 1512, 912, "Go Back", (1523, 918), 2)
    play_back_button = Button(160, 58, 1632, 1076, "Go Back", (1643, 1082), 2)

    def __post_init__(self):
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )


if __name__ == "__main__":
    v = GameVisual()
    v.test_draw()
