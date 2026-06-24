import pygame
from typing import Dict

from pacman.ui import Colors


class MenuVisualMixin:
    def draw_loading():
        pass

    def draw_hero(self) -> None:
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.pacman_img, (383, 0))
        self.draw_button(self.start_button, self.start_font)
        self.draw_button(self.instruction_button, self.button_font)
        self.draw_button(self.score_button, self.button_font)
        self.draw_button(self.exit_button, self.button_font)
        self.draw_text(
            "A lovely project by bpasquer & hliu",
            self.text_font,
            Colors.B_YELLOW.value,
            (875, 1094),
        )

    def draw_instruction(self) -> None:
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.white_frame, (365, 208))
        pygame.draw.rect(
            self.screen,
            Colors.WHITE.value,
            (401, 258, 1356, 778),
            border_radius=30,
        )
        self.draw_text(
            "Instruction", self.title_font, Colors.D_BLUE.value, (461, 298)
        )
        self.draw_text(
            "Try not to get eaten by aggressive ghosts.\nYou will be moved to "
            "next level if you last",
            self.t_font,
            Colors.D_BLUE.value,
            (700, 402),
        )
        self.draw_text(
            "60 seconds!", self.t_font, Colors.RED.value, (1400, 440)
        )
        self.draw_text(
            "Use the arrow keys to move Pac-Man ",
            self.t_font,
            Colors.D_BLUE.value,
            (700, 534),
        )
        self.draw_text("up, down", self.t_font, Colors.RED.value, (1307, 534))
        self.draw_text(
            "left, and right ", self.t_font, Colors.RED.value, (700, 572)
        )
        self.draw_text(
            "inside the mize.", self.t_font, Colors.D_BLUE.value, (950, 572)
        )
        self.draw_text(
            "Small dot (pac-gum) = \nBig dot (super-gum) = \nAfter eating "
            "super-gum, ghosts become vulnerable, \nIt's time to eat them up! "
            "Each ghost = ",
            self.t_font,
            Colors.D_BLUE.value,
            (700, 666),
        )
        self.draw_text("point,", self.t_font, Colors.D_BLUE.value, (1115, 666))
        self.draw_text("point,", self.t_font, Colors.D_BLUE.value, (1115, 704))
        self.draw_text("point,", self.t_font, Colors.D_BLUE.value, (1412, 780))
        self.draw_text("10", self.t_font, Colors.RED.value, (1070, 666))
        self.draw_text("50", self.t_font, Colors.RED.value, (1068, 704))
        self.draw_text("200", self.t_font, Colors.RED.value, (1346, 780))
        self.draw_text(
            "Try to survive and collect as many points!\nHave fun!!",
            self.t_font,
            Colors.D_BLUE.value,
            (700, 874),
        )

        self.screen.blit(self.instruc_img, (461, 503))
        self.draw_button(self.go_back_button, self.button_font)

    def draw_type_name(self) -> None:
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.white_frame, (365, 208))
        pygame.draw.rect(
            self.screen,
            Colors.WHITE.value,
            (401, 258, 1356, 778),
            border_radius=30,
        )
        self.draw_text(
            "Congratulations !!!",
            self.start_font,
            Colors.D_BLUE.value,
            (779, 322),
        )
        self.draw_text(
            "Let us know what your name is...",
            self.title_font,
            Colors.D_BLUE.value,
            (681, 436),
        )
        self.draw_text(
            "__________", self.title_font, Colors.D_BLUE.value, (938, 531)
        )
        self.screen.blit(self.type_name_img, (828, 678))
        self.draw_button(self.go_back_button, self.button_font)

    def draw_score_list(self, scores: Dict[str, int]) -> None:
        offset = 55
        nb_dashes = {}
        sorted_scores = dict(
            sorted(scores.items(), key=lambda x: x[1], reverse=True)
        )
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.white_frame, (365, 208))
        pygame.draw.rect(
            self.screen,
            Colors.WHITE.value,
            (401, 258, 1356, 778),
            border_radius=30,
        )
        self.draw_text(
            "Here are the best players...",
            self.title_font,
            Colors.D_BLUE.value,
            (743, 348),
        )
        for name in scores.keys():
            total = 17
            nb_dash = total - len(name)
            nb_dashes[name] = nb_dash
        i = 0
        for name, score in sorted_scores.items():
            self.draw_text(
                f"{name} {'-' * nb_dashes[name]}",
                self.button_font,
                Colors.D_BLUE.value,
                (743, 434 + offset * i),
            )
            self.draw_text(
                f"{score}",
                self.button_font,
                Colors.D_BLUE.value,
                (1069, 434 + offset * i),
            )
            i += 1
        self.screen.blit(self.score_img, (1208, 460))
        self.draw_button(self.go_back_button, self.button_font)

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
