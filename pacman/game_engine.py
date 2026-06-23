#! /usr/bin/env python3

import pygame
from .game_visual import GameVisual
from .utils.engine_utils import GameState, EngineUtils
from typing import Any


class GameEngine:

    def handle_events(self, game: GameVisual, state: GameState) -> bool:
        next_button = game.draw_next_button()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if next_button.collidepoint(mouse_pos):
                    state.current_level += 1
                    state.reset_level()

        return True

    def render(
        self,
        game: GameVisual,
        state: GameState,
        config: dict[str, Any],
    ) -> None:
        game.screen.fill(game.colors.BLACK.value)

        game.draw_stats(state)

        game.draw_maze(state)

        game.draw_pacman(state)

        game.draw_pacgums(state)

        game.draw_next_button()

        pygame.display.flip()

    def init_game(self, config: dict[str, Any]) -> None:
        game = GameVisual()

        pygame.init()
        pygame.display.set_caption("Pac-Man")

        state = GameState(config=config)

        game.main_menu()

        clock = pygame.time.Clock()
        running = True

        utils = EngineUtils()

        while running:
            dt = clock.tick(60)
            state.level_timer += dt

            # when 1 sec passed
            if state.level_timer >= 1000:
                state.level_timer = 0
                state.statistics.time_left -= 1

                if state.statistics.time_left <= 0:
                    # handle game over
                    pass

            running = self.handle_events(game, state)

            utils.update_animation(state, dt)
            utils.update_direction(state)
            utils.update_pacman_target(state)
            utils.move_pacman(state)

            self.render(game, state, config)

        pygame.quit()
