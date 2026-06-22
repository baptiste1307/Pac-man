#! /usr/bin/env python3

import pygame
from dataclasses import dataclass
from .game_stats import GameStats
from .game_visual import GameVisual
from .visual_utils import Level
from typing import Any


class GameEngine:
    def get_levels(self, config: dict[str, Any]) -> list[Level]:
        levels: list[Level] = []

        for level in config["levels"]:
            new_level = Level(width=level["width"], height=level["height"])
            levels.append(new_level)

        return levels

    def init_game(self, config: dict[str, Any]) -> None:
        v = GameVisual()

        pygame.init()
        levels = self.get_levels(config)

        pygame.display.set_caption("Pac-Man")

        v.main_menu()
        current_level = 0

        clock = pygame.time.Clock()
        running = True

        while running:
            next_button = v.draw_next_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if next_button.collidepoint(mouse_pos):
                        current_level += 1

                        if current_level >= len(levels):
                            current_level = 0

            v.screen.fill(v.colors.BLACK.value)

            v.draw_stats(config, current_level)

            v.draw_maze(
                levels[current_level].maze.maze,
                levels[current_level].cell_size,
            )

            v.screen.blit(
                # function to load pacman
                v.load_pacman(
                    levels[current_level].maze.maze,
                    levels[current_level].cell_size,
                ),
                # coordinates where to draw it
                (300, 300),
            )

            next_button = v.draw_next_button()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
