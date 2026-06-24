#! /usr/bin/env python3

import pygame
from pacman.core import GameState
from pacman.visual import GameVisual
from .engine_utils import EngineUtils
from typing import Any


class GameEngine:

    def handle_events(self, game: GameVisual, state: GameState) -> bool:
        next_button = game.draw_next_button()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if next_button.collidepoint(mouse_pos):
                    state.current_level += 1
                    state.reset_level()

            if event.type == pygame.VIDEORESIZE:
                game.resize(event.w, event.h)
                state.refresh_layout()

        return True

    def render(
        self,
        game: GameVisual,
        state: GameState,
    ) -> None:
        # game.screen.fill(game.colors.BLACK.value)

        # game.draw_stats(state)

        game.draw_maze(state)

        game.draw_pacman(state)

        game.draw_pacgums(state)

        game.draw_ghosts(state)

        game.draw_next_button()

        game.present()

    def init_game(self, config: dict[str, Any]) -> None:
        game = GameVisual()

        pygame.init()
        pygame.display.set_caption("Pac-Man")

        state = GameState(config=config, game=game)

        utils = EngineUtils()
        clock = pygame.time.Clock()
        game.test_draw()
        running = True

        while running:
            dt = clock.tick(60)
            state.level_timer += dt

            # when 1 sec passed
            if state.level_timer >= 1000:
                state.level_timer = 0
                state.statistics.time_left -= 1

                if state.statistics.time_left <= 0:
                    state.statistics.lives -= 1
                    if state.statistics.lives <= 0:
                        # handle game over
                        pass

            running = self.handle_events(game, state)
            game.draw_play(state)

            utils.update_animation(state, dt)
            utils.update_direction(state)
            utils.update_pacman_target(state)
            utils.move_pacman(state)

            self.render(game, state)

        pygame.quit()
