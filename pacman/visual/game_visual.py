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
    screen_width, screen_height = 2160, 1280
    info = pygame.display.Info()
    scaled_width, scaled_height = 500, 500

    scaled_screen = pygame.display.set_mode((scaled_width, scaled_height))
    screen: Any = pygame.Surface((screen_width, screen_height))

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

    def test_draw(self):
        page = "hero"
        scores = {"huian": 300, "baptiste": 600, "allan": 200}
        running = True
        data = [1, 3, 60, 234]
        while running:
            for event in pygame.event.get():
                event_pos = self.get_real_mouse_pos()
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if page == "hero":
                        if pygame.Rect(self.start_button.rect).collidepoint(
                            event_pos
                        ):
                            page = "play"
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
                            running = False
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
            self.scaled_surface = pygame.transform.smoothscale(self.screen, (self.scaled_width, self.scaled_height))
            self.scaled_screen.blit(self.scaled_surface, (0, 0))
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    v = GameVisual()
    v.test_draw()
