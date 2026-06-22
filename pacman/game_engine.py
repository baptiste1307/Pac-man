#! /usr/bin/env python3

import pygame
from .game_visual import GameVisual
from .utils.engine_utils import GameState, EngineUtils
from typing import Any
from .assets import LoadedAssets


class GameEngine:

    def render(
        self,
        game: GameVisual,
        assets: LoadedAssets,
        state: GameState,
        config: dict[str, Any],
    ) -> None:
        game.screen.fill(game.colors.BLACK.value)

        game.draw_stats(config, state.current_level)

        game.draw_maze(
            state.current_maze,
            state.current_cell_size,
        )

        game.draw_pacman(
            direction=state.direction,
            x=state.pacman_x,
            y=state.pacman_y,
            cell_size=state.current_cell_size,
            assets=assets,
            current_frame=state.current_frame,
        )

        game.draw_next_button()

        pygame.display.flip()

    def init_game(self, config: dict[str, Any]) -> None:
        game = GameVisual()
        assets = LoadedAssets()

        pygame.init()
        pygame.display.set_caption("Pac-Man")

        state = GameState(config=config)

        game.main_menu()

        clock = pygame.time.Clock()
        running = True

        utils = EngineUtils()

        while running:
            dt = clock.tick(60)

            running = utils.handle_events(game, state)

            utils.update_animation(state, dt)
            utils.update_direction(state)
            utils.update_pacman_target(state)
            utils.move_pacman(state)

            self.render(game, assets, state, config)

        pygame.quit()
