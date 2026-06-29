import pygame
from typing import Dict

from pacman.ui import Colors

HERO_POSITIONS = {
    "pacman": (383, 0),
    "credit": (875, 1094),
}

MENU_FRAME_POS = (365, 208)
MENU_PANEL_RECT = (401, 258, 1356, 778)
MENU_PANEL_RADIUS = 30

INSTRUCTION_POSITIONS = {
    "title": (461, 298),
    "intro": (700, 402),
    "time": (1400, 440),
    "move_text": (700, 534),
    "up_down": (1307, 534),
    "left_right": (700, 572),
    "maze_text": (950, 572),
    "points_text": (700, 666),
    "small_point": (1115, 666),
    "super_point": (1115, 704),
    "ghost_point": (1412, 780),
    "small_value": (1070, 666),
    "super_value": (1068, 704),
    "ghost_value": (1346, 780),
    "ending": (700, 874),
    "keyboard": (461, 503),
}

TYPE_NAME_POSITIONS = {
    "title": (779, 322),
    "subtitle": (681, 436),
    "line": (938, 531),
    "image": (828, 678),
}

SCORE_POSITIONS = {
    "title": (743, 348),
    "name": (743, 434),
    "score": (1069, 434),
    "image": (1208, 460),
}

SCORE_ROW_OFFSET = 55
SCORE_NAME_DASH_TOTAL = 17


class MenuVisualMixin:
    def draw_loading():
        pass

    def draw_hero(self) -> None:
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.pacman_img, self.pos(HERO_POSITIONS["pacman"]))
        self.draw_button(self.start_button, self.start_font)
        self.draw_button(self.instruction_button, self.button_font)
        self.draw_button(self.score_button, self.button_font)
        self.draw_button(self.exit_button, self.button_font)
        self.draw_text(
            "A lovely project by bpasquer & hliu",
            self.text_font,
            Colors.B_YELLOW.value,
            HERO_POSITIONS["credit"],
        )

    def draw_instruction(self) -> None:
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.white_frame, self.pos(MENU_FRAME_POS))
        pygame.draw.rect(
            self.screen,
            Colors.WHITE.value,
            self.rect(MENU_PANEL_RECT),
            border_radius=self.radius(MENU_PANEL_RADIUS),
        )
        self.draw_text(
            "Instruction",
            self.title_font,
            Colors.D_BLUE.value,
            INSTRUCTION_POSITIONS["title"],
        )
        self.draw_text(
            "Try not to get eaten by aggressive ghosts.\nYou will be moved to "
            "next level if you last",
            self.t_font,
            Colors.D_BLUE.value,
            INSTRUCTION_POSITIONS["intro"],
        )
        self.draw_text(
            "60 seconds!",
            self.t_font,
            Colors.RED.value,
            INSTRUCTION_POSITIONS["time"],
        )
        self.draw_text(
            "Use the arrow keys to move Pac-Man ",
            self.t_font,
            Colors.D_BLUE.value,
            INSTRUCTION_POSITIONS["move_text"],
        )
        self.draw_text(
            "up, down",
            self.t_font,
            Colors.RED.value,
            INSTRUCTION_POSITIONS["up_down"],
        )
        self.draw_text(
            "left, and right ",
            self.t_font,
            Colors.RED.value,
            INSTRUCTION_POSITIONS["left_right"],
        )
        self.draw_text(
            "inside the mize.",
            self.t_font,
            Colors.D_BLUE.value,
            INSTRUCTION_POSITIONS["maze_text"],
        )
        self.draw_text(
            "Small dot (pac-gum) = \nBig dot (super-gum) = \nAfter eating "
            "super-gum, ghosts become vulnerable, \nIt's time to eat them up! "
            "Each ghost = ",
            self.t_font,
            Colors.D_BLUE.value,
            INSTRUCTION_POSITIONS["points_text"],
        )
        self.draw_text(
            "point,",
            self.t_font,
            Colors.D_BLUE.value,
            INSTRUCTION_POSITIONS["small_point"],
        )
        self.draw_text(
            "point,",
            self.t_font,
            Colors.D_BLUE.value,
            INSTRUCTION_POSITIONS["super_point"],
        )
        self.draw_text(
            "point,",
            self.t_font,
            Colors.D_BLUE.value,
            INSTRUCTION_POSITIONS["ghost_point"],
        )
        self.draw_text(
            "10",
            self.t_font,
            Colors.RED.value,
            INSTRUCTION_POSITIONS["small_value"],
        )
        self.draw_text(
            "50",
            self.t_font,
            Colors.RED.value,
            INSTRUCTION_POSITIONS["super_value"],
        )
        self.draw_text(
            "200",
            self.t_font,
            Colors.RED.value,
            INSTRUCTION_POSITIONS["ghost_value"],
        )
        self.draw_text(
            "Try to survive and collect as many points!\nHave fun!!",
            self.t_font,
            Colors.D_BLUE.value,
            INSTRUCTION_POSITIONS["ending"],
        )

        self.screen.blit(
            self.instruc_img,
            self.pos(INSTRUCTION_POSITIONS["keyboard"]),
        )
        self.draw_button(self.go_back_button, self.button_font)

    def draw_type_name(self) -> None:
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.white_frame, self.pos(MENU_FRAME_POS))
        pygame.draw.rect(
            self.screen,
            Colors.WHITE.value,
            self.rect(MENU_PANEL_RECT),
            border_radius=self.radius(MENU_PANEL_RADIUS),
        )
        self.draw_text(
            "Congratulations !!!",
            self.start_font,
            Colors.D_BLUE.value,
            TYPE_NAME_POSITIONS["title"],
        )
        self.draw_text(
            "Let us know what your name is...",
            self.title_font,
            Colors.D_BLUE.value,
            TYPE_NAME_POSITIONS["subtitle"],
        )
        self.draw_text(
            "__________",
            self.title_font,
            Colors.D_BLUE.value,
            TYPE_NAME_POSITIONS["line"],
        )
        self.screen.blit(
            self.type_name_img,
            self.pos(TYPE_NAME_POSITIONS["image"]),
        )
        self.draw_button(self.go_back_button, self.button_font)

    def draw_score_list(self, scores: Dict[str, int]) -> None:
        nb_dashes = {}
        sorted_scores = dict(
            sorted(scores.items(), key=lambda x: x[1], reverse=True)
        )
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.white_frame, self.pos(MENU_FRAME_POS))
        pygame.draw.rect(
            self.screen,
            Colors.WHITE.value,
            self.rect(MENU_PANEL_RECT),
            border_radius=self.radius(MENU_PANEL_RADIUS),
        )
        self.draw_text(
            "Here are the best players...",
            self.title_font,
            Colors.D_BLUE.value,
            SCORE_POSITIONS["title"],
        )
        for name in scores.keys():
            nb_dash = SCORE_NAME_DASH_TOTAL - len(name)
            nb_dashes[name] = nb_dash
        i = 0
        for name, score in sorted_scores.items():
            row_y = SCORE_POSITIONS["name"][1] + SCORE_ROW_OFFSET * i
            self.draw_text(
                f"{name} {'-' * nb_dashes[name]}",
                self.button_font,
                Colors.D_BLUE.value,
                (SCORE_POSITIONS["name"][0], row_y),
            )
            self.draw_text(
                f"{score}",
                self.button_font,
                Colors.D_BLUE.value,
                (SCORE_POSITIONS["score"][0], row_y),
            )
            i += 1
        self.screen.blit(self.score_img, self.pos(SCORE_POSITIONS["image"]))
        self.draw_button(self.go_back_button, self.button_font)
